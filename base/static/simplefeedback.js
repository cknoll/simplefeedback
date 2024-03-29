// An example annotation we'll add/remove via JavaScript
const csrftoken = Cookies.get('csrftoken');
const target = {
    re_app: 'simplefeedback',
};


const fetch_params = {...target, ...{_format: 'recogito'}};
const baseUrl = window.location.origin;
const url = new URL("/api/get/", baseUrl)
url.search = new URLSearchParams(fetch_params)
fetchUrl = url.toString()
console.log(url.toString());

var rc = [];

var r = Recogito.init({
content: 'annotation_content', // Element id to attach to
locale: 'de',
mode: 'pre',
widgets: [
    'COMMENT',
    { widget: 'TAG', vocabulary: [ 'Place', 'Person', 'Event', 'Organization', 'Animal' ] }
],
relationVocabulary: [ 'isRelated', 'isPartOf', 'isSameAs ']
});

loadAnnotations = (url) => fetch(url)
.then(response => response.json()).then(annotations => {
    //r.setAnnotations(annotations);
    console.log(annotations);
    const clones = annotations.map(a => a.clone());


    return "OK";
    // return this.highlighter.init(clones).then(() =>
    // this.relationsLayer.init(clones));

});


//r.loadAnnotations(fetchUrl);


var ann = {"@context":"http://www.w3.org/ns/anno.jsonld","type":"Annotation","body":[{"type":"TextualBody","value":"foo","purpose":"commenting"}],"target":{"selector":[{"type":"TextQuoteSelector","exact":"commodo"},{"type":"TextPositionSelector","start":230,"end":237}]},"id":"#888ddfb9-a391-42c6-8dc1-9f569c4526dc"};


r.setAnnotations([

]);


// r.on('selectAnnotation', function(a) {
//   console.log('selected', a);
// });

r.on('createAnnotation', function(a) {
console.log('created', a);
var re_id = a['id'].slice(1);
var new_annotation = {
    re_id: re_id,
}
var merged = {
    ...target,
    ...new_annotation,
    re_payload: a
}

rc.push(merged);

const merged_json = JSON.stringify(merged);
console.log(merged_json);

// note: fetch returns a promise.

/*
# currently we do not want to send every comment
var res = fetch('/api/add/', {
    method: 'POST', // or 'PUT'
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken
    },
    body: merged_json,
});

rc.push(res);
*/
//console.log(res);


// .then(response => response.json())
// .then(merged => {
//   console.log('Success:', merged);
// })
// .catch((error) => {
//   console.error('Error:', error);
// });

});

r.on('updateAnnotation', function(annotation, previous) {
console.log('updated', previous, 'with', annotation);
});


document.getElementById('mainSubmit').addEventListener('click', function() {
console.log("pressed submit");

var annotationList = r.getAnnotations();
var reviewerName = document.getElementById("reviewerName").value;

// TODO: submit button should only be enabled if name is valid and annotation list is non-empty
if (annotationList.length == 0) {
    alert("No annotations to submit");
    return
}
if (reviewerName.trim() == "") {
    alert("Invalid revier name");
    return
}

var doc_key = JSON.parse(document.getElementById("doc_key").textContent);
var merged = {
    ...target,
    doc_key: doc_key,
    reviewer_name: reviewerName,
    re_annotation_list: annotationList
}

const merged_json = JSON.stringify(merged);
console.log(merged_json);

// send all annotations at once
var res = fetch('/api/add/', {
    method: 'POST', // or 'PUT'
    headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken
    },
    body: merged_json,
});


});
