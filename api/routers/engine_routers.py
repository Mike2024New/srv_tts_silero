from fastapi import APIRouter, status
from config import SayRequest, ApiStartParameters
from engine.main import Engine


def routers_factory(engine: Engine) -> APIRouter:
    router = APIRouter()

    @router.get('/parameters/')
    def parameters():
        """Получить параметры модели. Узнать запущен ли движок."""
        return {
            'running': engine.is_running(),
            'parameters': engine.get_parameters(),
        }

    @router.post('/start/', status_code=status.HTTP_200_OK)
    async def start(input_parameters: ApiStartParameters):
        """Запуск движка с передачей параметров"""
        engine.start(parameters=input_parameters)
        return {'result': 'Engine запущен'}

    @router.post('/execute/', status_code=status.HTTP_200_OK)
    async def execute(say_request: SayRequest):
        """Воспроизведение аудио через http."""
        await engine.say(text=say_request.text, speaker=say_request.speaker, add=say_request.add)
        return {'result': 'Текст воспроизводится'}

    @router.get('/interrupt/', status_code=status.HTTP_200_OK)
    async def interrupt():
        await engine.interrupt()
        return {'result': 'Воспроизведение текста остановлено'}

    @router.get('/stop/', status_code=status.HTTP_200_OK)
    async def stop():
        engine.stop()
        return {'result': 'Engine остановлен'}

    return router
