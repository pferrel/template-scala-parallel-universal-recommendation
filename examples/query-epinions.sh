#!/usr/bin/env bash

echo ""
echo "Recommendations for user: 1"
curl -H "Content-Type: application/json" -d '
{
    "user": "u1"
}' http://localhost:8000/queries.json
echo ""
#sleep 2

echo ""
echo "Recommendations for user: 2"
curl -H "Content-Type: application/json" -d '
{
    "user": "u2"
}' http://localhost:8000/queries.json
echo ""
#sleep 2

echo ""
echo "Recommendations for user: 3"
curl -H "Content-Type: application/json" -d '
{
    "user": "u3"
}' http://localhost:8000/queries.json
echo ""
#sleep 2

echo ""
echo "Recommendations for user: 4"
curl -H "Content-Type: application/json" -d '
{
    "user": "u4"
}' http://localhost:8000/queries.json
echo ""
#sleep 2

