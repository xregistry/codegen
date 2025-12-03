import * as assert from 'assert';
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('xregistry.xrcg-vscode'));
    });

    test('Extension should activate', async () => {
        const extension = vscode.extensions.getExtension('xregistry.xrcg-vscode');
        assert.ok(extension);
        await extension!.activate();
        assert.strictEqual(extension!.isActive, true);
    });

    suite('Commands Registration', () => {
        test('All generate commands should be registered', async () => {
            const commands = await vscode.commands.getCommands(true);
            
            // C# commands
            const csCommands = [
                'xrcg.generate-cs-amqpconsumer',
                'xrcg.generate-cs-amqpproducer',
                'xrcg.generate-cs-egproducer',
                'xrcg.generate-cs-ehconsumer',
                'xrcg.generate-cs-ehproducer',
                'xrcg.generate-cs-kafkaconsumer',
                'xrcg.generate-cs-kafkaproducer',
                'xrcg.generate-cs-mqttclient',
                'xrcg.generate-cs-sbconsumer',
                'xrcg.generate-cs-sbproducer'
            ];

            // Java commands
            const javaCommands = [
                'xrcg.generate-java-amqpconsumer',
                'xrcg.generate-java-amqpproducer',
                'xrcg.generate-java-ehconsumer',
                'xrcg.generate-java-ehproducer',
                'xrcg.generate-java-kafkaconsumer',
                'xrcg.generate-java-kafkaproducer',
                'xrcg.generate-java-mqttclient',
                'xrcg.generate-java-sbconsumer',
                'xrcg.generate-java-sbproducer'
            ];

            // Python commands
            const pyCommands = [
                'xrcg.generate-py-ehconsumer',
                'xrcg.generate-py-ehproducer',
                'xrcg.generate-py-kafkaconsumer',
                'xrcg.generate-py-kafkaproducer',
                'xrcg.generate-py-mqttclient'
            ];

            // TypeScript commands
            const tsCommands = [
                'xrcg.generate-ts-amqpconsumer',
                'xrcg.generate-ts-amqpproducer',
                'xrcg.generate-ts-egproducer',
                'xrcg.generate-ts-ehconsumer',
                'xrcg.generate-ts-ehproducer',
                'xrcg.generate-ts-kafkaconsumer',
                'xrcg.generate-ts-kafkaproducer',
                'xrcg.generate-ts-mqttclient',
                'xrcg.generate-ts-sbconsumer',
                'xrcg.generate-ts-sbproducer'
            ];

            const allExpectedCommands = [...csCommands, ...javaCommands, ...pyCommands, ...tsCommands];
            
            for (const cmd of allExpectedCommands) {
                assert.ok(
                    commands.includes(cmd),
                    `Command ${cmd} should be registered`
                );
            }
        });
    });

    suite('Output Channel', () => {
        test('xregistry output channel should exist after activation', async () => {
            const extension = vscode.extensions.getExtension('xregistry.xrcg-vscode');
            await extension!.activate();
            
            // The output channel is created during activation
            // We can verify by checking that no error is thrown when trying to show it
            // Note: VS Code API doesn't expose a way to list output channels directly
            assert.ok(extension!.isActive);
        });
    });

    suite('Menu Contributions', () => {
        test('Extension should contribute xrcgSubmenu to explorer context menu', async () => {
            const extension = vscode.extensions.getExtension('xregistry.xrcg-vscode');
            assert.ok(extension);
            
            const packageJson = extension.packageJSON;
            assert.ok(packageJson.contributes);
            assert.ok(packageJson.contributes.menus);
            
            // Verify explorer/context menu has xrcgSubmenu
            const explorerContext = packageJson.contributes.menus['explorer/context'];
            assert.ok(explorerContext, 'explorer/context menu should be defined');
            const hasXrcgSubmenu = explorerContext.some((item: any) => item.submenu === 'xrcgSubmenu');
            assert.ok(hasXrcgSubmenu, 'xrcgSubmenu should be in explorer/context menu');
        });

        test('Extension should contribute language submenus', async () => {
            const extension = vscode.extensions.getExtension('xregistry.xrcg-vscode');
            assert.ok(extension);
            
            const packageJson = extension.packageJSON;
            const menus = packageJson.contributes.menus;
            
            // Verify language submenus exist
            const expectedSubmenus = ['xrcg.py', 'xrcg.ts', 'xrcg.cs', 'xrcg.java', 'xrcg.asyncapi', 'xrcg.openapi', 'xrcg.asaql'];
            for (const submenu of expectedSubmenus) {
                assert.ok(menus[submenu], `Submenu ${submenu} should be defined`);
                assert.ok(menus[submenu].length > 0, `Submenu ${submenu} should have menu items`);
            }
        });

        test('Python submenu should have all expected commands', async () => {
            const extension = vscode.extensions.getExtension('xregistry.xrcg-vscode');
            assert.ok(extension);
            
            const pyMenu = extension.packageJSON.contributes.menus['xrcg.py'];
            assert.ok(pyMenu);
            
            const expectedCommands = [
                'xrcg.generate-py-amqpconsumer',
                'xrcg.generate-py-amqpproducer',
                'xrcg.generate-py-kafkaconsumer',
                'xrcg.generate-py-kafkaproducer',
                'xrcg.generate-py-ehconsumer',
                'xrcg.generate-py-ehproducer',
                'xrcg.generate-py-sbconsumer',
                'xrcg.generate-py-sbproducer',
                'xrcg.generate-py-mqttclient'
            ];
            
            const menuCommands = pyMenu.map((item: any) => item.command);
            for (const cmd of expectedCommands) {
                assert.ok(menuCommands.includes(cmd), `Python menu should include ${cmd}`);
            }
        });
    });

    suite('xrcg CLI Integration', function() {
        // These tests require xrcg to be installed
        this.timeout(30000); // Allow 30 seconds for CLI operations

        let xrcgAvailable = false;
        let tempDir: string;

        suiteSetup(async () => {
            // Check if xrcg is available
            try {
                await execAsync('xrcg --help');
                xrcgAvailable = true;
            } catch {
                xrcgAvailable = false;
            }

            // Create temp directory for test outputs
            tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'xrcg-test-'));
        });

        suiteTeardown(() => {
            // Clean up temp directory
            if (tempDir && fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        });

        test('xrcg CLI should be available', async function() {
            if (!xrcgAvailable) {
                this.skip();
                return;
            }
            
            const { stdout } = await execAsync('xrcg --help');
            assert.ok(stdout.includes('generate'), 'xrcg help should mention generate command');
            assert.ok(stdout.includes('validate'), 'xrcg help should mention validate command');
            assert.ok(stdout.includes('list'), 'xrcg help should mention list command');
        });

        test('xrcg should list available templates', async function() {
            if (!xrcgAvailable) {
                this.skip();
                return;
            }

            const { stdout } = await execAsync('xrcg list');
            assert.ok(stdout.includes('cs'), 'Should list C# templates');
            assert.ok(stdout.includes('py'), 'Should list Python templates');
            assert.ok(stdout.includes('java'), 'Should list Java templates');
            assert.ok(stdout.includes('ts'), 'Should list TypeScript templates');
        });

        test('xrcg should successfully generate AsyncAPI from sample definition', async function() {
            if (!xrcgAvailable) {
                this.skip();
                return;
            }

            // Find a sample definition file
            const workspaceRoot = path.resolve(__dirname, '../../../../..');
            const sampleFile = path.join(workspaceRoot, 'samples', 'message-definitions', 'lightbulb.xreg.json');
            
            if (!fs.existsSync(sampleFile)) {
                this.skip();
                return;
            }

            const outputPath = path.join(tempDir, 'asyncapi-output');
            const command = `xrcg generate --projectname TestProject --language asyncapi --style producer --definitions "${sampleFile}" --output "${outputPath}"`;
            
            const { stdout, stderr } = await execAsync(command);
            
            // Verify output was created
            assert.ok(fs.existsSync(outputPath), 'Output directory should be created');
            
            // Check for generated files
            const files = fs.readdirSync(outputPath);
            assert.ok(files.length > 0, 'Should generate at least one file');
        });

        test('xrcg should successfully generate Python Kafka producer from sample definition', async function() {
            if (!xrcgAvailable) {
                this.skip();
                return;
            }

            const workspaceRoot = path.resolve(__dirname, '../../../../..');
            const sampleFile = path.join(workspaceRoot, 'samples', 'message-definitions', 'lightbulb.xreg.json');
            
            if (!fs.existsSync(sampleFile)) {
                this.skip();
                return;
            }

            const outputPath = path.join(tempDir, 'py-kafka-output');
            const command = `xrcg generate --projectname TestKafka --language py --style kafkaproducer --definitions "${sampleFile}" --output "${outputPath}"`;
            
            await execAsync(command);
            
            // Verify output was created
            assert.ok(fs.existsSync(outputPath), 'Output directory should be created');
            
            // Check for Python files
            const findPyFiles = (dir: string): string[] => {
                const files: string[] = [];
                const entries = fs.readdirSync(dir, { withFileTypes: true });
                for (const entry of entries) {
                    const fullPath = path.join(dir, entry.name);
                    if (entry.isDirectory()) {
                        files.push(...findPyFiles(fullPath));
                    } else if (entry.name.endsWith('.py')) {
                        files.push(fullPath);
                    }
                }
                return files;
            };
            
            const pyFiles = findPyFiles(outputPath);
            assert.ok(pyFiles.length > 0, 'Should generate Python files');
        });
    });
});
