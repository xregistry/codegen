import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

const currentVersionMajor = 0;
const currentVersionMinor = 13;
const currentVersionPatch = 0;

async function checkXRegistryTool(context: vscode.ExtensionContext, outputChannel: vscode.OutputChannel): Promise<boolean> {
    // Check if xregistry CLI is available
    try {
        return await execShellCommand('xrcg --version', outputChannel)
            .then((stdout) => {
                const versionMatch = stdout.match(/(\d+)\.(\d+)\.(\d+)/);
                if (!versionMatch) {
                    return false;
                }
                const major = parseInt(versionMatch[1]);
                const minor = parseInt(versionMatch[2]);
                const patch = parseInt(versionMatch[3]);
                if (major < currentVersionMajor) {
                    vscode.window.showWarningMessage('xregistry tool version is outdated. Please update.');
                    return false;
                }
                return true;
            })
            .catch(async (error) => {
                const installOption = await vscode.window.showWarningMessage(
                    'xregistry tool is not available. Do you want to install it?', 'Yes', 'No');
                if (installOption === 'Yes') {
                    await execShellCommand('pip install xrcg', outputChannel);
                    vscode.window.showInformationMessage('xregistry tool has been installed successfully.');
                    return true;
                }
                return false;
            });
    } catch (error) {
        vscode.window.showErrorMessage('Error checking xregistry tool availability: ' + error);
        return false;
    }
}

function execShellCommand(cmd: string, outputChannel?: vscode.OutputChannel): Promise<string> {
    return new Promise((resolve, reject) => {
        const process = exec(cmd, (error, stdout, stderr) => {
            if (error) {
                reject(error);
            } else {
                resolve(stdout ? stdout : stderr);
            }
        });
        if (outputChannel) {
            process.stdout?.on('data', (data) => {
                outputChannel.append(data.toString());
            });
            process.stderr?.on('data', (data) => {
                outputChannel.append(data.toString());
            });
        }
    });
}

function executeCommand(command: string, outputPath: vscode.Uri | null, outputChannel: vscode.OutputChannel) {
    exec(command, (error, stdout, stderr) => {
        if (error) {
            outputChannel.appendLine(`Error: ${error.message}`);
            vscode.window.showErrorMessage(`Error: ${stderr}`);
        } else {
            outputChannel.appendLine(stdout);
            if (outputPath) {
                if (fs.existsSync(outputPath.fsPath)) {
                    const stats = fs.statSync(outputPath.fsPath);
                    if (stats.isFile()) {
                        vscode.workspace.openTextDocument(outputPath).then((document) => {
                            vscode.window.showTextDocument(document);
                        });
                    } else if (stats.isDirectory()) {
                        vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(outputPath.fsPath), true);
                    }
                }
            } else {
                vscode.workspace.openTextDocument({ content: stdout }).then((document) => {
                    vscode.window.showTextDocument(document);
                });
            }
            vscode.window.showInformationMessage(`Success: ${stdout}`);
        }
    });
}

export function activate(context: vscode.ExtensionContext) {
    const disposables: vscode.Disposable[] = [];
    (async () => {
        const outputChannel = vscode.window.createOutputChannel('xregistry');

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-amqpconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-amqpconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style amqpconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-amqpproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-amqpproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style amqpproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-egproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-egproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style egproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-ehconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-ehconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style ehconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-ehproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-ehproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style ehproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-kafkaconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-kafkaconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style kafkaconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-kafkaproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-kafkaproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style kafkaproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-mqttclient', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-mqttclient');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style mqttclient --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-sbconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-sbconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style sbconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-sbproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-sbproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style sbproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-openapi-producer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-openapi-producer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language openapi --style producer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-openapi-subscriber', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-openapi-subscriber');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language openapi --style subscriber --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-amqpconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-amqpconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style amqpconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-amqpproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-amqpproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style amqpproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-ehconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-ehconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style ehconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-ehproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-ehproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style ehproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-kafkaconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-kafkaconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style kafkaconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-kafkaproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-kafkaproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style kafkaproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-mqttclient', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-mqttclient');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style mqttclient --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-sbconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-sbconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style sbconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-sbproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-sbproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style sbproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-dashboard', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-dashboard');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style dashboard --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-ehconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-ehconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style ehconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-kafkaconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-kafkaconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style kafkaconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-kafkaproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-kafkaproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style kafkaproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-egazfn', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-egazfn');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style egazfn --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-ehazfn', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-ehazfn');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style ehazfn --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-cs-sbazfn', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-cs-sbazfn');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language cs --style sbazfn --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-asaql-dispatch', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-asaql-dispatch');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language asaql --style dispatch --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-asaql-dispatchpayload', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-asaql-dispatchpayload');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language asaql --style dispatchpayload --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-asyncapi-consumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-asyncapi-consumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language asyncapi --style consumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-asyncapi-producer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-asyncapi-producer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language asyncapi --style producer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-amqpconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-amqpconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style amqpconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-amqpjmsproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-amqpjmsproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style amqpjmsproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-amqpproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-amqpproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style amqpproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-ehconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-ehconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style ehconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-ehproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-ehproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style ehproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-kafkaconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-kafkaconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style kafkaconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-kafkaproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-kafkaproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style kafkaproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-mqttclient', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-mqttclient');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style mqttclient --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-producer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-producer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style producer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-sbconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-sbconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style sbconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-java-sbproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-java-sbproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language java --style sbproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-py-producer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-py-producer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language py --style producer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-amqpconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-amqpconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style amqpconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-amqpproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-amqpproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style amqpproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-egproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-egproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style egproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-ehproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-ehproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style ehproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-mqttclient', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-mqttclient');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style mqttclient --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-producerhttp', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-producerhttp');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style producerhttp --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-sbconsumer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-sbconsumer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style sbconsumer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        disposables.push(vscode.commands.registerCommand('xrcg.generate-ts-sbproducer', async (uri: vscode.Uri) => {
            if (!await checkXRegistryTool(context, outputChannel)) { return; }
            const filePath = uri.fsPath;
            const outputPathSuggestion = getSuggestedOutputPath(filePath, '{input_file_name}-ts-sbproducer');
            const outputPath = await vscode.window.showSaveDialog({ defaultUri: vscode.Uri.file(outputPathSuggestion), saveLabel: 'Save Output', filters : { 'All Files': ['*'] } });
            if (!outputPath) { return; }
            const command = `xrcg generate --projectname ${path.basename(outputPath.fsPath)} --language ts --style sbproducer --definitions ${filePath} --output ${outputPath.fsPath}`;
            executeCommand(command, outputPath, outputChannel);
        }));

        context.subscriptions.push(...disposables);
    })();
}

export function deactivate() {}

function getSuggestedOutputPath(inputFilePath: string, suggestedOutputPath: string) {
    const inputFileName = inputFilePath ? path.basename(inputFilePath, path.extname(inputFilePath)) : '';
    const outFileName = suggestedOutputPath.replace('{input_file_name}', inputFileName);
    return path.join(path.dirname(inputFilePath), outFileName);
}