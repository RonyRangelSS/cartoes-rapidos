# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from random import randint

dict = {
'Qual a ligação presente na molécula da água?': 'Ligação covalente', 
'Por que a água é considerada um solvente universal?': 'Porque consegue absorver uma grande quantidade de solutos',
'O que é água destilada ?': 'É a água que não possui sais minerais dissolvidos',
'O que é água mineral ?': 'É a água proveniente de minérios',
'Em qual família o Carbono se encontra?': 'Família um A',
'Em qual período da tabela periódica o Carbono está?': 'Período quatro',
'Qual o número atômico do Carbono?': 'nove',
'Em qual ordem o parafuso Telúrico foi organizado?': 'Ordem crescente de massa atômico',
'Por que o parafuso telúrico não teve futuro na área da ciência?':'Ele não englobava todos os elementos químicos'
}

def perguntaResposta(json):
    numero = randint(1, 9)
    chaves = list(json.keys())
    valores = list(json.values())
    return [chaves[numero], valores[numero]]

def perguntar(json):
    numero = randint(1, 9)
    chaves = list(json.keys())
    return chaves[numero]

def responder(json):
    numero = randint(1, 9)
    valores = list(json.values())
    return valores[numero]


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Olá, Cartões Rápidos é uma skill gamificada feita para auxiliar seus estudos. O que você deseja fazer?"
        session_attr = handler_input.attributes_manager.session_attributes       
        session_attr['qtdPerguntas'] = 0
        session_attr['acertos'] = 0

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class QuestionarioIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("QuestionarioIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        quiz = perguntaResposta(dict)
        questao = quiz[0]
        session_attr['resposta'] = quiz[1]
        session_attr['qtdPerguntas'] += 1
        
        speak_output = f"OK, vou iniciar o questionário. {questao}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class RespostaIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RespostaIntent")(handler_input)
    
    def handle(self, handler_input):
        resposta = ask_utils.request_util.get_slot(handler_input, 'resposta')
        session_attr = handler_input.attributes_manager.session_attributes
        
        if resposta and resposta.value:
            resposta = resposta.value
            respostaQuiz = session_attr['resposta'].lower()
            
            if resposta == respostaQuiz:
                speak_output = "Muito bem! O que você deseja fazer agora?"
                session_attr['acertos'] += 1
            else:
                speak_output = f"A resposta na planilha é {respostaQuiz}. Você acertou?"
                return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        
        else: 
            speak_output = "Desculpe, não consegui identificar a sua resposta. Por favor, tente novamente."
            return handler_input.response_builder.speak(speak_output).response

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class ErroIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ErroIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Que pena, na próxima você consegue. O que deseja fazer agora?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
class AcertoIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AcertoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = "Muito bem! O que deseja fazer agora?"
        session_attr['acertos'] += 1

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class ProximaPerguntaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ProximaPerguntaIntent")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        quiz = perguntaResposta(dict)
        questao = quiz[0]
        session_attr['resposta'] = quiz[1]
        session_attr['qtdPerguntas'] += 1
        
        speak_output = f"{questao}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
class FinalizarRevisaoIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FinalizarRevisaoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Tudo bem! Depois você continua"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

        

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(QuestionarioIntentHandler())
sb.add_request_handler(RespostaIntentHandler())
sb.add_request_handler(AcertoIntentHandler())
sb.add_request_handler(ErroIntentHandler())
sb.add_request_handler(ProximaPerguntaIntentHandler())
sb.add_request_handler(FinalizarRevisaoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()