import uvicorn
import sys

if __name__ == "__main__":
    print("=" * 60)
    print(" Starting Universal Document AI Parser Web Server")
    print(" Categories: Academic, Identity, Professional, Other")
    print(" Accessible at: http://127.0.0.1:8000")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
