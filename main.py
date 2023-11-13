from fastapi import FastAPI
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from contextlib import asynccontextmanager
from os import environ

from endpoints.article import router as article_router
from endpoints.comments import router as comments_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    endpoint = environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        exporter = OTLPSpanExporter(endpoint=endpoint)
        tracer.add_span_processor(
            BatchSpanProcessor(exporter)
    )
    yield

app = FastAPI(docs_url='/api/community/docs', redoc_url='/api/community/redoc', openapi_url='/api/community/openapi.json', lifespan=lifespan)
app.include_router(article_router, prefix="/api/community/article")
app.include_router(comments_router, prefix="/api/community/article")


resource = Resource(attributes={
    "service.name": "community-service"
})

tracer = TracerProvider(resource=resource)

FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
HTTPXClientInstrumentor().instrument(tracer_provider=tracer)