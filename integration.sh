#!/usr/bin/env bash
set -euo pipefail

TIMEOUT=${INTEGRATION_TIMEOUT:-60}
BASE_URL="http://localhost:3000"

echo "==> Submitting job..."
RESPONSE=$(curl -sf -X POST "${BASE_URL}/submit")
JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

echo "==> Polling for completion (timeout: ${TIMEOUT}s)..."
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
  STATUS=$(curl -sf "${BASE_URL}/status/${JOB_ID}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','unknown'))")
  echo "Status: $STATUS (${ELAPSED}s elapsed)"
  if [ "$STATUS" = "completed" ]; then
    echo "==> Integration test PASSED: job completed successfully"
    exit 0
  fi
  sleep 2
  ELAPSED=$((ELAPSED + 2))
done

echo "==> Integration test FAILED: job did not complete within ${TIMEOUT}s"
exit 1