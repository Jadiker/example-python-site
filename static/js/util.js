export function jsonify(data) {
    var object = {};
    data.forEach(function(value, key){
        object[key] = value;
    });
    return JSON.stringify(object);
}
