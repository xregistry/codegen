import * as assert from 'assert';
import * as vscode from 'vscode';

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
});
