// import Highlighter from './Highlighter.js';
const csrftoken = Cookies.get('csrftoken');

const doc_key = JSON.parse(document.getElementById("doc_key").textContent);
const owner_key = JSON.parse(document.getElementById("owner_key").textContent);

const baseUrl = window.location.origin;
const fetchFeedbacksUrl = new URL(`/api/get/fb/${owner_key}`, baseUrl)
const fetchAnnotationsUrl = new URL(`/api/get/ann/${owner_key}`, baseUrl)


var sac = document.getElementById("show_annotations_content");
var hl = new Highlighter(sac, null);

// this object was for debugging
// var ann =  {
//     "@context":"http://www.w3.org/ns/anno.jsonld",
//     "type":"Annotation",
//     "body":[
//         {"type":"TextualBody","value":"comment1 like model","purpose":"commenting"}
//     ],
//     "target":
//     {
//         "selector":[
//             {"type":"TextQuoteSelector","exact":"document"},
//             {"type":"TextPositionSelector","start":32,"end":40}
//         ]
//     },
//     "id":"#95937184-078a-49c0-8037-d8495b593674",
//     "start":2,
//     "end":27
// };

var annotationArray = {};
var annotationList = [];
var annotationListIndex = null;
var activeAnnotationSpans = null;


// prepare detail display in right colum
const reviewDetailMetaDiv = document.getElementById('review-detail-meta');
const reviewDetailContentDiv = document.getElementById('review-detail-content');


function resetActiveAnnotationSpans(){
  if (activeAnnotationSpans === null) return;

  activeAnnotationSpans.forEach(span => {
    span.classList.remove("unique-active-annotation-hl");
    span.classList.add("annotation-hl");
  });
}

function setActiveAnnotationSpans(annSpans) {
  activeAnnotationSpans = annSpans;
  activeAnnotationSpans.forEach(span => {
    span.classList.remove("annotation-hl");
    span.classList.add("unique-active-annotation-hl");
  });

}

function handleClickEvent(span) {
  /*
  * This is a separate function because triggering span.click() has
  * unintended sideeffects in nested spans
  */

  // one span was clicked, but multiple spans might be affected
  // get all relevant spans
  const annId = span.id.split("--")[0];

  // convert from live collection to an ordinary list
  const annSpans = Array.from(document.getElementsByClassName(`ann-${annId}`));

  resetActiveAnnotationSpans();
  setActiveAnnotationSpans(annSpans);

  // Get the content of the clicked span element (currently not used)
  // const spanContent = span.textContent;

  // display the annotation content in the left column
  const ann = annotationArray[annId]
  reviewDetailMetaDiv.textContent = `Reviewer: ${ann.feedback.reviewer}, ${ann.feedback.date}`;
  reviewDetailContentDiv.textContent = `${ann.comment_value}`;
}


function annClickHandler(span) {
  const handler = (() => {
    handleClickEvent(span);
  });
  return handler;
};


// function to create the event listeners (must be called after the annotations are loaded)
function connectAnnotationSpans(){
    const relevantSpans = document.querySelectorAll('.annotation-hl');
    // Attach a click event listener to each span element
    relevantSpans.forEach(span => {
      span.addEventListener('click', annClickHandler(span))
      span.addEventListener('mouseover', annClickHandler(span))
    });
};

function activateNextAnnotation(){

  if (annotationListIndex === null){
    annotationListIndex = 0;
  } else {
    annotationListIndex += 1;
    annotationListIndex %= annotationList.length;
  }
  activateIndexedAnnotation(annotationListIndex);
}

function activatePrevAnnotation(){

    if (annotationListIndex === null){
      annotationListIndex = annotationList.length - 1;
    } else {
      // prevent getting negative numbers
      annotationListIndex += annotationList.length - 1;
      annotationListIndex %= annotationList.length;
    }
  activateIndexedAnnotation(annotationListIndex);
}

function activateIndexedAnnotation(annotationListIndex){
  /*
  * one annotation can consist of multiple span-elements
  */
  const ann = annotationList[annotationListIndex];
  const spans = document.getElementsByClassName(`ann-${ann.pk}`)
  // var span = document.getElementById(ann.pk);
  // console.log(annotationListIndex, span);

  // obsolete
  // spans.forEach((span, idx) => {
  //   span.click();
  // });

  // trigger click event only on one element (which will handle all the other spans)
  if (spans.length) {
    handleClickEvent(spans[0]);
  }

}



// do some asynchronous work
const a = (async () => {
    const fixedAnnotations = (await fetch(fetchAnnotationsUrl).then((response) => response.json()));

    await hl.init(fixedAnnotations);
    connectAnnotationSpans();

    //make annotations easily available
    fixedAnnotations.forEach(ann => annotationArray[ann.pk] = ann);
    annotationList = Object.values(annotationArray);
    annotationList.sort((a, b) => a.start - b.start);

  })();


// useful snippets for debugging
// var fr = (await fetch("http://localhost:8000/api/get").then((response) => response.json()))[1];
//hl.addOrUpdateAnnotation(ann);
