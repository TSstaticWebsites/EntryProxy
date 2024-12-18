from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.options("/relay")
async def options_relay():
    return Response(
        content="",
        headers={
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "https://onion-browser-proxy-inzpir1h.devinapps.com",
            "Access-Control-Allow-Credentials": "true",
        }
    )

@router.post("/relay")
async def relay_package(request: Request):
    """
    Simply forward the encrypted package without any server-side crypto operations.
    The package is expected to be pre-encrypted by the client.
    """
    try:
        # Forward the encrypted package as-is
        package = await request.body()
        return Response(content=package)
    except Exception as e:
        return Response(
            content=str(e),
            status_code=500
        )
