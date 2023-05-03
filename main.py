import uuid

from flask import Flask, request, jsonify, abort

# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]


# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/todo-list', methods=['POST'])
def handleNewListEntrie():
    newList = request.get_json(force=True)
    if not newList:
        abort(400, "Keine Daten in der Liste.")
    for listItem, value in newList.items():
        if listItem == "name":
            if value is "":
                abort(400, "Die Liste benötigt ein Namen.")
    print("New Todo-List will be added: {}".format(newList))


@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handlelist(list_id):
    list_by_id = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_by_id = l
            break
    if not (list_by_id):
        abort(404)
    if request.method == 'GET':
        print("Found List with id: {} ".format(list_id))
        return jsonify([i for i in todos if i['list'] == list_id])
    if request.method == 'DELETE':
        print("Deleting Todo-List with id : {}".format(list_id))
        todo_lists.remove(list_by_id)
        return '', 200


@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def handleNewListItemEntrie(list_id):
    newitem = request.get_json(force=True)
    if not newitem:
        abort(400, "Keine Daten in der Liste.")
    if newitem['name'] == "":
        abort(400, "Bitte Item-Name angeben.")
    list_by_id = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_by_id = l
            break
    if not (list_by_id):
        abort(404)
    itemForList = {}
    itemForList['id'] = uuid.uuid4()
    for i in todos:
        if i['id'] == itemForList['id']:
            abort(404, "Fehler bei der erstellung der UUID.")
    itemForList['name'] = newitem['name']
    itemForList['description'] = newitem['description']
    itemForList['list'] = list_by_id['id']
    todos.append(itemForList)
    print("New items will be added: {}".format(itemForList))
    return itemForList, 200


@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def editListItemEntry(list_id, entry_id):
    newitem = request.get_json(force=True)
    edited = None
    if not newitem:
        abort(400, "Keine Daten in der Liste.")
    if newitem['name'] == "":
        abort(400, "Bitte Item-Name angeben.")
    for l in todos:
        if str(l['id']) == entry_id and str(l['list']) == list_id:
            edited = l
            break
    edited['name'] = newitem['name']
    edited['description'] = newitem['description']
    print("Item mit der Id: {} wurde editiert: {}".format(edited['id'], edited))
    return edited, 200


@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def deleteListItemEntry(list_id, entry_id):
    for i in todos:
        if str(i['id']) == entry_id and str(i['list'] == list_id):
            todos.remove(i)
            return "Item erfolgreich gelöscht", 200
    abort(404, "Fehlerhafte Ids")


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
