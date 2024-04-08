// import Highlighter from './Highlighter.js';
const csrftoken = Cookies.get('csrftoken');

const doc_key = JSON.parse(document.getElementById("doc_key").textContent);
const owner_key = JSON.parse(document.getElementById("owner_key").textContent);

const baseUrl = window.location.origin;
const fetchFeedbacksUrl = new URL(`/api/get/fb/${owner_key}`, baseUrl)
const fetchAnnotationsUrl = new URL(`/api/get/ann/${owner_key}`, baseUrl)


var sac = document.getElementById("show_annotations_content");
var hl = new Highlighter(sac, null);
var ann =  {
    "@context":"http://www.w3.org/ns/anno.jsonld",
    "type":"Annotation",
    "body":[
        {"type":"TextualBody","value":"comment1 like model","purpose":"commenting"}
    ],
    "target":
    {
        "selector":[
            {"type":"TextQuoteSelector","exact":"document"},
            {"type":"TextPositionSelector","start":32,"end":40}
        ]
    },
    "id":"#95937184-078a-49c0-8037-d8495b593674",
    "start":2,
    "end":27
};


// prepare detail display in right colum
const reviewDetailMetaDiv = document.getElementById('review-detail-meta');
const reviewDetailContentDiv = document.getElementById('review-detail-content');

function annClickHandler(span) {
  const handler = (() => {
    // Get the content of the clicked span element
    const spanContent = span.textContent;
    reviewDetailContentDiv.textContent = spanContent;
  });
  return handler;
};


// function to create the event listeners (must be called after the annotations are loaded)
function connectAnnotationSpans(){
    const relevantSpans = document.querySelectorAll('.annotation-hl');
    // Attach a click event listener to each span element
    relevantSpans.forEach(span => {
      span.addEventListener('click', annClickHandler(span))
    });
};


// do some asynchronous work
const a = (async () => {
    const fixedAnnotations = (await fetch(fetchAnnotationsUrl).then((response) => response.json()));

    await hl.init(fixedAnnotations);
    connectAnnotationSpans();
  })();


// useful snippets for debugging
// var fr = (await fetch("http://localhost:8000/api/get").then((response) => response.json()))[1];
//hl.addOrUpdateAnnotation(ann);
