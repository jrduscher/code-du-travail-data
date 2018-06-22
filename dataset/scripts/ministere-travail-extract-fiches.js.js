const fetch = require("node-fetch");
const serialExec = require("promise-serial-exec");
const JSDOM = require("jsdom").JSDOM;

const FICHES_URLS = require("./ministere-travail-liste-fiches");

const qsa = (node, selector) => Array.from(node.querySelectorAll(selector));

const parseFiche = url =>
  JSDOM.fromURL(url).then(dom => {
    const article = qsa(dom.window.document, ".main-article")[0];
    const title = qsa(article, "h1")[0].textContent.trim();
    const text = qsa(article, ".main-article__texte")[0].textContent.trim();
    const summary = qsa(dom.window.document, ".navigation-article li")
      .map(n => n.textContent.trim())
      .filter(t => t !== "L’INFO EN PLUS" && t !== "POUR ALLER PLUS LOIN");
    const articles = qsa(
      dom.window.document,
      "article.encarts__article li"
    ).map(n => ({
      url: qsa(n, "a") && qsa(n, "a")[0] && qsa(n, "a")[0].getAttribute("href"),
      text: n.textContent.trim()
    }));
    return {
      title,
      text,
      summary,
      articles
    };
  });

serialExec(
  FICHES_URLS.map(f => () => parseFiche(f.url).catch()).filter(Boolean)
)
  .then(j => console.log(JSON.stringify(j, null, 2)))
  .catch(console.log);
