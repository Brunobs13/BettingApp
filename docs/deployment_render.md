# Deploy on Render (Quick Guide)

1. Create a new Web Service in Render from:
- `https://github.com/Brunobs13/BettingApp_Object-Oriented-Programming`

2. Runtime settings:
- Environment: `Docker`
- Port: `8080`

3. Environment variables:
- `LOG_LEVEL=INFO`
- `BETTING_LOG_PATH=artifacts/events.jsonl`
- `BETTING_RANDOM_SEED=42`

4. Deploy and open generated URL.

5. Verify endpoints:
- `/health`
- `/api/state`
