// import Highlighter from './Highlighter.js';
const csrftoken = Cookies.get('csrftoken');


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

hl.addOrUpdateAnnotation(ann);


// // do some asynchronous work (use `await a`)
// const a = (async () => {
//     const fixedAnnotation = (await fetch("http://localhost:8000/api/get").then((response) => response.json()))[1];
//     const range = document.createRange();
//     const selector = fixedAnnotation.target.selector.filter(a => a.type == 'TextPositionSelector')[0]


//     // range.setStart(ac, selector.start);
//     // range.setEnd(ac, selector.end);

//     // nontrivial problem: find the correct start-nodes + offset
//     range.setStart(sac, 1);
//     range.setEnd(sac, 3);

//     var span_wrapper = document.createElement('SPAN');
//     range.surroundContents(span_wrapper);
//     span_wrapper.className = "r6o-annotation";

//     return fixedAnnotation
//   })()
