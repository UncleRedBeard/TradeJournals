import model from "@site-model";

export function GET() {
  return new Response(JSON.stringify(model.searchEntries), {
    headers: { "content-type": "application/json; charset=utf-8" }
  });
}
