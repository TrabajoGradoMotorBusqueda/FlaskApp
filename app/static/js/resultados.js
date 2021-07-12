const BASE_API = 'http://localhost:5000';
const BASE_URL =  window.location.origin + window.location.pathname


function investigacionItemTemplate(index, investigacion, relacionados = false) {
  let index_text = index + 1;
  let id = investigacion.id;
  let titulo = investigacion.titulo.toUpperCase();
  let anio =
    investigacion.anio_convocatoria != null
      ? investigacion.anio_convocatoria
      : '';
  let resumen = investigacion.resumen;
  let keywords =
    investigacion.palabras_clave.length > 0
      ? investigacion.palabras_clave.join(', ')
      : 'No Registradas';
  let autores = investigacion.autores
    .map((autor) => {
      return '<li>' + autor + '</li>';
    })
    .join('\n');
  let asesores = '';
  if (investigacion.asesores != undefined) {
    asesores = `
            <h5 class="d-inline">${
              investigacion.asesores.length > 1 ? 'Asesores' : 'Asesor'
            }: </h5>${investigacion.asesores.join(' ,')}.
            <br>
        `;
  }
  let facultad_text =
    investigacion.facultades.length > 1 ? 'Facultades' : 'Facultad';
  let facultades = investigacion.facultades.join(' ,');
  let programas_text =
    investigacion.programas.length > 1 ? 'Programas' : 'Programa';
  let programas = investigacion.programas.join(' ,');
  let grupos_text =
    investigacion.grupos_investigacion.length > 1
      ? 'Grupos de Investigacion'
      : 'Grupo de Investigacion';
  let grupos = investigacion.grupos_investigacion.join(' ,');
  let lineas_text =
    investigacion.lineas_investigacion.length > 1
      ? 'Lineas de Investigacion'
      : 'Linea de Investigacion';
  let lineas = investigacion.lineas_investigacion.join(' ,');
  let button_relacionados = relacionados
    ? ''
    : `<button type="button" onclick="investigacionesRelacionadas(${id})" class="btn btn-success social-links social-icons related-${id}" style="background-color: #28a745;" data-toggle="modal" data-target="#InvestigacionesRelacionadas">Investigaciones Relacionadas</button>`;

  return `
    <div class="sl-item">
        <div class="sl-left number-circle"><strong>${index_text}</strong></div>
        <div class="sl-right">
            <div id="${id}" data-id="${id}">
                <h3>
                    <a class="link"data-toggle="collapse" href="#investigacion-${id}">
                        ${titulo}
                    </a>
                </h3>
                <div class="collapse" id="investigacion-${id}">
                    <blockquote class="m-t-10">
                        <h5>Resumen: </h5>
                        <p>
                            ${resumen}
                        </p>
                        <h5 class="d-inline">Palabras Clave: </h5>
                        ${keywords}.
                    </blockquote>
                    <div>
                        <h5>Autores: </h5>
                        <ul>
                            ${autores}
                        </ul>
                    </div>
                    ${asesores}
                    <h5 class="d-inline">${facultad_text}: </h5> ${facultades}.
                    <br>
                    <h5 class="d-inline">${programas_text}: </h5> ${programas}.
                    <br>
                    <h5 class="d-inline">${grupos_text}: </h5> ${grupos}.
                    <br>
                    <h5 class="d-inline">${lineas_text}: </h5> ${lineas}.
                    <br>
                    <h5 class="d-inline">Tipo Convocatoria: </h5> ${investigacion.tipo_convocatoria}
                    <br>
                    <h5 class="d-inline">Año Convocatoria: </h5> ${anio}
                    <div class="d-flex flex-row-reverse" id="buttons-${id}">
                      <button type="button" class="btn btn-success social-links social-icons pdf-${id}" data-id="${id}" style="background-color: #28a745;"><i class="fas fa-file-download"></i></button>
                      ${button_relacionados}
                    </div>
                </div>
            </div>
        </div>
        <hr>
    </div>
    `;
}
function createTemplate(HTMLstring) {
  const html = document.implementation.createHTMLDocument();
  html.body.innerHTML = HTMLstring;
  return html.body.children[0];
}

function renderResultadosInvestigaciones(
  investigaciones,
  $container,
  pageNumber
) {
  if ($container.children.length > 0) {
    $container.innerHTML = '';
  }
  investigaciones.forEach((investigacion, index) => {
    let index_result = index + (pageNumber - 1) * 10;
    const HTMLString = investigacionItemTemplate(index_result, investigacion);
    const investigacionElement = createTemplate(HTMLString);

    $container.append(investigacionElement);
    $('.pdf-' + investigacion.id).on('click', function () {
      let $container_investigacion = document.getElementById(investigacion.id);
      html2pdf($container_investigacion);
    });
  });
}

function renderInvestigacionesRelacionadas(investigaciones) {
  const $container_related = document.querySelector('.modal-body');
  const $title_modal = document.querySelector('.modal-title');

  $title_modal.innerHTML = investigaciones.investigacion.titulo
  if ($container_related.children.length > 0) {
    $container_related.innerHTML = '';
  }
  investigaciones.relacionados.forEach((investigacion, index) => {
    const HTMLString = investigacionItemTemplate(
      index,
      investigacion,
      (relacionados = true)
    );
    const investigacionElement = createTemplate(HTMLString);

    $container_related.append(investigacionElement);
    $('.pdf-' + investigacion.id).on('click', function () {
      let $container_investigacion = document.getElementById(investigacion.id);
      html2pdf($container_investigacion);
    });

  });
}

const investigacionesRelacionadas = async (id) => {
  console.log('join Related');
  const endpoint = '/relacionados/';

  const getData = async (url) => {
    const response = await fetch(url);
    const data = await response.json();

    if (data.relacionados.length > 0) {
      return data;
    } else {
      throw new Error('No se encontro ningun resultado');
    }
  }
  // Consultar Busqueda
  const relacionados = await getData(BASE_API + endpoint + id);

  // Renderizar Resultados
  renderInvestigacionesRelacionadas(relacionados);
}

function paginateResults(data, paginator, resultsContainer) {
  paginator.pagination({
    dataSource: data,
    pageSize: 10,
    showPageNumbers: true,
    showPrevious: true,
    showNext: true,
    showNavigator: true,
    showGoInput: true,
    showGoButton: true,
    goButtonText: 'Ir',
    className: 'paginationjs-theme-green paginationjs-big',
    callback: function (data, pagination) {
      renderResultadosInvestigaciones(
        data,
        resultsContainer,
        pagination.pageNumber
      );
    },
    afterRender: function () {
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    },
  });
}

const find_results = (async function load() {
  const endpoint = '/busqueda/';

  async function getData(url) {
    const response = await fetch(url);
    const data = await response.json();

    if (data.investigaciones.length > 0) {
      return data;
    } else {
      throw new Error('No se encontro ningun resultado');
    }
  }

  // Consultar Busqueda
  const params = new URLSearchParams(window.location.search);
  const query = params.get('query');
  const resultados = await getData(BASE_API + endpoint + query);

  const $resultsContainer = document.querySelector('.profiletimeline');
  // const $resultsContainer = $('.profiletimeline');
  const $paginator = $('#paginator');
  paginateResults(resultados.investigaciones, $paginator, $resultsContainer);
  // renderResultadosInvestigaciones(
  //   resultados.investigaciones,
  //   $resultsContainer
  // );
})();


(
  function searchBar(){
  $('#nav-input-search').on('keyup', async function (event){
    if (event.keyCode === 13) {
    event.preventDefault();
    const endpoint = '/busqueda/';

    async function getData(url) {
      const response = await fetch(url);
      const data = await response.json();

      if (data.investigaciones.length > 0) {
        return data;
      } else {
        throw new Error('No se encontro ningun resultado');
      }
    }

    // Consultar Busqueda
    const query =this.value;

    const resultados = await getData(BASE_API + endpoint + query);

    // Actualizar URL
    let params = new URLSearchParams(window.location.search);
    params.set('query', query)

    const next_url = BASE_URL + '?' + params.toString()
    const next_title = 'Thaqhana |'+ query
    const nextState = { additionalInformation: 'Update URL' };
    window.history.pushState(nextState, next_title, next_url);
    window.history.replaceState(nextState, next_title, next_url);
    document.title = next_title

    const $resultsContainer = document.querySelector('.profiletimeline');
    // const $resultsContainer = $('.profiletimeline');
    const $paginator = $('#paginator');
    paginateResults(resultados.investigaciones, $paginator, $resultsContainer);
  }
  })
  $('#nav-icon-search').on('click', async function (event){
    event.preventDefault();
    const endpoint = '/busqueda/';

    async function getData(url) {
      const response = await fetch(url);
      const data = await response.json();

      if (data.investigaciones.length > 0) {
        return data;
      } else {
        throw new Error('No se encontro ningun resultado');
      }
    }

    // Consultar Busqueda
    const query = $('#nav-input-search')[0].value;
    const resultados = await getData(BASE_API + endpoint + query);

    // Actualizar URL
    let params = new URLSearchParams(window.location.search);
    params.set('query', query)

    const next_url = BASE_URL + '?' + params.toString()
    const next_title = 'Thaqhana |'+ query
    const nextState = { additionalInformation: 'Update URL' };
    window.history.pushState(nextState, next_title, next_url);
    window.history.replaceState(nextState, next_title, next_url);
    document.title = next_title


    const $resultsContainer = document.querySelector('.profiletimeline');
    // const $resultsContainer = $('.profiletimeline');
    const $paginator = $('#paginator');
    paginateResults(resultados.investigaciones, $paginator, $resultsContainer);
  })
}
)();


