function investigacionItemTemplate(index, investigacion) {
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
                      <button type="button" class="btn btn-success social-links social-icons" style="background-color: #28a745;" data-toggle="modal" data-target="#dialogo1">Investigaciones Relacionadas</button>
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
      $container_investigacion = document.getElementById(investigacion.id);
      html2pdf($container_investigacion)
    });
  });
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
    }
  });
}

(async function load() {
  console.log('join');
  const BASE_API = 'http://localhost:5000/busqueda/';

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
  const resultados = await getData(BASE_API + query);

  const $resultsContainer = document.querySelector('.profiletimeline');
  // const $resultsContainer = $('.profiletimeline');
  const $paginator = $('#paginator');
  paginateResults(resultados.investigaciones, $paginator, $resultsContainer);
  // renderResultadosInvestigaciones(
  //   resultados.investigaciones,
  //   $resultsContainer
  // );
})();
