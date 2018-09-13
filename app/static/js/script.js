try{
    var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
    var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
    var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent;
    var recognition;// = new SpeechRecognition();

}catch(e){
    console.error(e);
}

$(document).ready(escutar());

function escutar(){
  recognition = new SpeechRecognition();

	recognition.interimResults = false;
  recognition.lang = 'pt-BR';

    recognition.start();

    recognition.onresult = function(event) {
        var speechResult = event.results[0][0].transcript;

        $(idCampoTexto).val(speechResult);

        /*Simula o click para a aplicação recuperar o texto da fala e exibir na tela*/
        $(idCampoTexto).click();

        let termos = speechResult.split(" ");

        termos.forEach((termo) => {
          if(!isNaN(termo)){
            $(idCampoParametro).val(termo);
          }
        });

        var accessToken ="8ba4090b2183436c9149915d85d570b4";
        var baseUrl = "https://api.dialogflow.com/v1/";
        var text = $(idCampoTexto).val();

        var dataTemp = new Date();
        var pad = "00"
        var dataTime = dataTemp.getFullYear();
        dataTime += pad.substring(dataTemp.getMonth().toString().length) + (dataTemp.getMonth() + 1);
        dataTime += pad.substring(dataTemp.getDate().toString().length) + dataTemp.getDate();

        $.ajax({
          type: 'POST',
          url: baseUrl + "query?v=" + dataTime,
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          headers: {
              "Authorization": "Bearer " + accessToken
          },
          data: JSON.stringify({ query: text, lang: "pt-br", sessionId: userID }),
          success: function(data) {
              try{
              	$(idCampoResposta).val(data.result.fulfillment.speech);
              	$(idCampoAction).val(data.result.action);

                console.log(data.result.fulfillment.speech);
                console.log(data.result.action);
                var synth = window.speechSynthesis;
                if (speechSynthesis.onvoiceschanged !== undefined) {
                  speechSynthesis.onvoiceschanged = synth.getVoices()[15];
                }
                if (synth.speaking) {
                    console.error('speechSynthesis.speaking');
                    return;
                }
                if ($(idCampoResposta).val() !== '') {
                  var utterThis = new SpeechSynthesisUtterance(data.result.fulfillment.speech);
                  utterThis.pitch = 1.4;
                  utterThis.rate = 1.2;

                  $(idCampoResposta).click();

                  console.log('nome do usuario ' + userName);
                  console.log('id da imagem ' + idImagem);

                  synth.speak(utterThis);


                  var tempoResposta = setInterval(function(){
                  	clearInterval(tempoResposta);

                   // Simula o click para disparar o evento de teste da action na a aplicação (GX)
                  	$(idCampoAction).click();

                    recognition.stop();
                  	escutar();
                  }, 5000);

                  //HACK: Verificar porque as vezes chama a função e as vezes não
                  // utterThis.onend = function(event){
                  // 	console.log('end ' + event.elapsedTime + ' milliseconds.');

                  // 	$(idCampoAction).click();

                  //   recognition.stop();
                  // 	escutar();
                  // }

                  utterThis.onmark = function(event){
                  	console.log('mark' + event.elapsedTime + ' milliseconds.');
                  }
                  utterThis.onerror = function(event){
                  	console.log('error ' + event.elapsedTime + ' milliseconds.');
                  }
                  utterThis.onpause = function(event){
                  	console.log('pause ' + event.elapsedTime + ' milliseconds.');
                  }


                }
              }catch(e){
                console.log(e);
              }
          },
          error: function () {
              console.log('Not working yet');
          }
        });

    }
    recognition.onspeechend = function() {
        recognition.stop();
    }
    recognition.onerror = function(event) {console.log(event)}

    /* Tratamento de erro */
    recognition.onaudioend = function(event) {recognition.stop()}

    recognition.onend = function(event) {recognition.stop()}

    recognition.onsoundend = function(event) {recognition.stop()}

};
