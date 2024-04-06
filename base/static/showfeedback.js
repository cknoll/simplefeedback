const csrftoken = Cookies.get('csrftoken');

var sac = document.getElementById("show_annotations_content");

// do some asynchronous work (use `await a`)
const a = (async () => {
    const fixedAnnotation = (await fetch("http://localhost:8000/api/get").then((response) => response.json()))[1];
    const range = document.createRange();
    const selector = fixedAnnotation.target.selector.filter(a => a.type == 'TextPositionSelector')[0]


    // range.setStart(ac, selector.start);
    // range.setEnd(ac, selector.end);

    // nontrivial problem: find the correct start-nodes + offset
    range.setStart(sac, 1);
    range.setEnd(sac, 3);

    var span_wrapper = document.createElement('SPAN');
    range.surroundContents(span_wrapper);
    span_wrapper.className = "r6o-annotation";

    return fixedAnnotation
  })()
