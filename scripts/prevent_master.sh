BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" == "master" ]]; then
  >&2 echo "Cannot commit or push to master";
  exit 1;
fi