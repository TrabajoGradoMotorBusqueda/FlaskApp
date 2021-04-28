let resultados;
function load_results(data) {
  resultados = data;
}

const row_result = document.getElementById('row-results');

//Creamos un nuevo elemetno que se va a agregar al HTML
function createTemplate(HTMLstring) {
  const html = document.implementation.createHTMLDocument();
  html.body.innerHTML = HTMLstring;
  return html.body.children[0];
}

//Plantilla CARD
const card_result = function (title, status, keywords) {
  let string_keywords = '';
  keywords.forEach((word, i) => {
    i !== keywords.length - 1
      ? (string_keywords += ''.concat(word, ' - '))
      : (string_keywords += ''.concat(word, '.'));
  });
  return `
    <div id="col-result" class="col-md-4 d-flex justify-content-center">
        <div id="card-result" class="card">
            <div id="card-result-title">
                <h5 class="text-center">${title}</h5>
            </div>
            <div id="card-result-data" class="card-body d-flex flex-column">
                <div id="card-authors">
                    <!--<h6 class="text-muted mb-2">Autores</h6>-->
                    <h6 class="mb-2">Autores</h6>
                    <p>- David Santiago Pinchao Ortiz<br>- Doyoung de NCT<br></p>
                </div>
                <div id="card-program" >
                    <h6 class="mb-2">Programa</h6>
                    <p>${status}</p>
                </div>
                <div id="card-keywords">
                    <h6 class="mb-2">Palabras Clave</h6>
                    <p>${string_keywords}</p>
                </div>
                <a id="card-show" class="card-link align-self-center" data-bss-hover-animate="pulse" href="#" data-toggle="modal" data-target="#testmodal">
                    Ver más
                </a>
            </div>
        </div>
    </div>
    `;
};

let test = createTemplate(card_result('Uno', 'dos', ['a', 'b', 'c']));
row_result.append(test);

let f = createTemplate(card_result('Titulo', 'asdjasd', ['a', 'b', 'c']));
row_result.append(f);

let z = createTemplate(card_result('Titulo', 'asdjasd', ['a', 'b', 'c']));
row_result.append(z);
