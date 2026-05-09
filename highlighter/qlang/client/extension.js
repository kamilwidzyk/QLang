const vscode = require("vscode");
const { LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } = require("vscode-languageclient");

let client;

function activate(context) {
  console.log("QLang extension active");

  // Get configuration
  const config = vscode.workspace.getConfiguration("qlang");
  const pythonPath = config.get("server.path", "python");
  const serverArgs = config.get("server.args", ["language_server.py"]);

  // Server options
  const serverOptions = {
    command: pythonPath,
    args: serverArgs,
    options: {
      cwd: vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri.fsPath : undefined
    }
  };

  // Client options
  const clientOptions = {
    documentSelector: [{ scheme: "file", language: "qlang" }],
    synchronize: {
      fileEvents: vscode.workspace.createFileSystemWatcher("**/*.ql")
    }
  };

  // Create and start the client
  client = new LanguageClient("qlangLanguageServer", "QLang Language Server", serverOptions, clientOptions);
  client.start();

  context.subscriptions.push(client);
}

function deactivate() {
  if (client) {
    return client.stop();
  }
}

module.exports = {
  activate,
  deactivate
};