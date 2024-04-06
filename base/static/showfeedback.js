// import Highlighter from './Highlighter.js';
const csrftoken = Cookies.get('csrftoken');

const doc_key = JSON.parse(document.getElementById("doc_key").textContent);
const owner_key = JSON.parse(document.getElementById("owner_key").textContent);

const baseUrl = window.location.origin;
const fetchUrl = new URL(`/api/get/o/${owner_key}`, baseUrl)


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

// do some asynchronous work (use `await a`)
const a = (async () => {
    const fixedAnnotations = (await fetch(fetchUrl).then((response) => response.json()));

    //hl.addOrUpdateAnnotation(fixedAnnotation);
    // hl.init([ann]);
    hl.init(fixedAnnotations);
  })()


// useful snippets for debugging
// var fr = (await fetch("http://localhost:8000/api/get").then((response) => response.json()))[1];
//hl.addOrUpdateAnnotation(ann);
