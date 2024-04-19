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
widgets: [
    'COMMENT',
],
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


// var ann = {"@context":"http://www.w3.org/ns/anno.jsonld","type":"Annotation","body":[{"type":"TextualBody","value":"foo","purpose":"commenting"}],"target":{"selector":[{"type":"TextQuoteSelector","exact":"commodo"},{"type":"TextPositionSelector","start":230,"end":237}]},"id":"#888ddfb9-a391-42c6-8dc1-9f569c4526dc"};
var ann =  {"@context":"http://www.w3.org/ns/anno.jsonld","type":"Annotation","body":[{"type":"TextualBody","value":"comment1 like model","purpose":"commenting"}],"target":{"selector":[{"type":"TextQuoteSelector","exact":"document"},{"type":"TextPositionSelector","start":32,"end":40}]},"id":"#95937184-078a-49c0-8037-d8495b593674"};

var ac = document.getElementById("annotation_content");

r.setAnnotations([]);


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


var submit_button_active = true;
var main_submit_button = document.getElementById('mainSubmit');

if (main_submit_button) {

    main_submit_button.addEventListener('click', function(event) {
        console.log("pressed submit", submit_button_active);
        event.preventDefault();
        if (submit_button_active == false){
            // TODO: handle the case that request was lost (e.g. timeout of 10s)
            console.log("request is already processed");
            return
        }

    var annotationList = r.getAnnotations();
    var reviewerName = document.getElementById("reviewerName").value;

    // TODO: submit button should only be enabled if name is valid and annotation list is non-empty
    if (annotationList.length == 0) {
        alert("No annotations to submit");
        return
    }
    if (reviewerName.trim() == "") {
        alert("Empty or invalid reviewer name");
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

    // disable fetch button to prevent sending multiple data multiple times
    submit_button_active = false;
    // send all annotations at once
    var res = fetch('/api/add/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: merged_json,
    }).then(function() {
        console.log("fetch completed");
        window.location.href = `${window.location.href}/done`;
    });


    console.log(res);
    console.log("fetch initialized");

    });

}


// only for test
addAnnotation = annotation => {
    try {
      const [ domStart, domEnd ] = this.charOffsetsToDOMPosition([ annotation.start, annotation.end ]);

      const range = document.createRange();
      range.setStart(domStart.node, domStart.offset);
      range.setEnd(domEnd.node, domEnd.offset);

    //   this.applyStyles(annotation, spans);
    //   this.bindAnnotation(annotation, spans);
    } catch (error) {
      console.warn('Could not render annotation')
      console.warn(error);
      console.warn(annotation.underlying);
    }
  }
