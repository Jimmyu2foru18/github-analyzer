import asyncio
from config import Config
from scanner_service import ScannerService

async def main():
    config = Config.from_yaml()
    config.validate()
    
    scanner = ScannerService(config)
    keyword = input("Enter keyword to scan: ").strip()
    if keyword:
        await scanner.scan_and_audit(keyword)

if __name__ == "__main__":
    asyncio.run(main())
