const connection = new Postmonger.Session();
let eventDefinitionKey;
let createdData = {};
let authTokens = {};
let body = {metadata:{}};
const selectExam = document.getElementById("select-examIdField");
const selectStatus = document.getElementById("select-statusAppointment");
const schema = {};

connection.trigger("ready");
connection.trigger("requestSchema");
connection.trigger("requestTokens");
connection.trigger("requestTriggerEventDefinition");
connection.trigger('updateButton', { button: 'next', text: 'done', enabled: false });

connection.on("requestedTriggerEventDefinition", function (eventDefinitionModel) {
  if (eventDefinitionModel) {
    eventDefinitionKey = eventDefinitionModel.eventDefinitionKey;
  }
});

connection.on("requestedSchema", function (response) {
  for (let item of response.schema) {
    schema[item.name] = "{{" + item.key + "}}";
  }

    // Após pegar todos os dados da DE, será preenchido nos seletores de opções examIdField
    Object.keys(schema).forEach(key => {
        if (key != 'undefined'){
          const option = document.createElement("option");
          option.value = key;
          option.textContent = key;
          selectExam.appendChild(option);
        }
    });


});

connection.on("initActivity", (data) => {
  createdData = { ...createdData, ...data };
  createdData.isConfigured = false;

});

function verificarSelecoes() {
  body["metadata"]['options_metadata'] = []
    
  if (selectExam.selectedIndex > 0 && selectStatus.selectedIndex > 0) {
    body["metadata"]['options_metadata'] = [
      {'status_consulta': selectStatus.selectedOptions[0].value} , 
      {'opcao_consulta': selectExam.selectedOptions[0].value}
    ]
    connection.trigger('updateButton', { button: 'next', text: 'done', enabled: true });
  } 
  else {
      connection.trigger('updateButton', { button: 'next', text: 'done', enabled: false });
  }
}

document.addEventListener("change", (event) => {
  const target = event.target;
  if (target.id === "select-examIdField" || target.id === "select-statusAppointment") {
    verificarSelecoes();
  }
});

connection.on("requestedTokens", onGetTokens);

function onGetTokens(tokens) {
  authTokens = tokens;
}


connection.on("clickedNext", () => {
  save();
});

const save = () => {
  createdData["metaData"] = createdData["metaData"] || {};
  createdData["metaData"].isConfigured = true;
  createdData["arguments"].execute.inArguments = [] // Resetar os inArguments de versões de jorndas anteriores
  createdData["arguments"].execute.inArguments.push(schema);
  createdData.arguments.execute.body = JSON.stringify(body)
  if(schema.undefined){
    delete schema.undefined;
  }

  // console.log('createdData', createdData)
  connection.trigger("updateActivity", createdData);
};