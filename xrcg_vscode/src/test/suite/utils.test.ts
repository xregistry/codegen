import * as assert from 'assert';
import * as path from 'path';
import { getSuggestedOutputPath, parseVersion, isVersionSufficient, buildGenerateCommand } from '../../utils';

suite('Utility Functions Test Suite', () => {
    
    suite('getSuggestedOutputPath', () => {
        test('should replace {input_file_name} with actual file name', () => {
            const inputPath = '/home/user/project/contoso-erp.json';
            const pattern = '{input_file_name}-cs-kafkaproducer';
            const result = getSuggestedOutputPath(inputPath, pattern);
            
            assert.strictEqual(
                result,
                path.join('/home/user/project', 'contoso-erp-cs-kafkaproducer')
            );
        });

        test('should handle Windows paths', () => {
            const inputPath = 'C:\\Users\\dev\\project\\events.json';
            const pattern = '{input_file_name}-java-ehproducer';
            const result = getSuggestedOutputPath(inputPath, pattern);
            
            assert.strictEqual(
                path.basename(result),
                'events-java-ehproducer'
            );
        });

        test('should handle empty input path', () => {
            const inputPath = '';
            const pattern = '{input_file_name}-py-mqttclient';
            const result = getSuggestedOutputPath(inputPath, pattern);
            
            assert.strictEqual(result, '-py-mqttclient');
        });

        test('should handle pattern without placeholder', () => {
            const inputPath = '/project/file.json';
            const pattern = 'output-folder';
            const result = getSuggestedOutputPath(inputPath, pattern);
            
            assert.strictEqual(
                result,
                path.join('/project', 'output-folder')
            );
        });

        test('should strip only the last file extension', () => {
            // Note: path.extname only strips the last extension
            // So myfile.xreg.json -> myfile.xreg (stripping .json)
            const inputPath = '/project/myfile.xreg.json';
            const pattern = '{input_file_name}-output';
            const result = getSuggestedOutputPath(inputPath, pattern);
            
            // Should strip .json, leaving myfile.xreg
            assert.ok(result.includes('myfile.xreg-output'));
        });
    });

    suite('parseVersion', () => {
        test('should parse simple version string', () => {
            const result = parseVersion('0.9.0');
            assert.deepStrictEqual(result, { major: 0, minor: 9, patch: 0 });
        });

        test('should parse version from command output', () => {
            const result = parseVersion('xrcg version 1.2.3');
            assert.deepStrictEqual(result, { major: 1, minor: 2, patch: 3 });
        });

        test('should parse version with prefix text', () => {
            const result = parseVersion('Version: 10.20.30-beta');
            assert.deepStrictEqual(result, { major: 10, minor: 20, patch: 30 });
        });

        test('should return null for invalid version string', () => {
            const result = parseVersion('no version here');
            assert.strictEqual(result, null);
        });

        test('should return null for empty string', () => {
            const result = parseVersion('');
            assert.strictEqual(result, null);
        });

        test('should parse first version if multiple present', () => {
            const result = parseVersion('from 1.0.0 to 2.0.0');
            assert.deepStrictEqual(result, { major: 1, minor: 0, patch: 0 });
        });
    });

    suite('isVersionSufficient', () => {
        test('should return true when versions are equal', () => {
            const actual = { major: 1, minor: 2, patch: 3 };
            const required = { major: 1, minor: 2, patch: 3 };
            assert.strictEqual(isVersionSufficient(actual, required), true);
        });

        test('should return true when actual major is higher', () => {
            const actual = { major: 2, minor: 0, patch: 0 };
            const required = { major: 1, minor: 9, patch: 9 };
            assert.strictEqual(isVersionSufficient(actual, required), true);
        });

        test('should return false when actual major is lower', () => {
            const actual = { major: 0, minor: 9, patch: 9 };
            const required = { major: 1, minor: 0, patch: 0 };
            assert.strictEqual(isVersionSufficient(actual, required), false);
        });

        test('should return true when actual minor is higher (same major)', () => {
            const actual = { major: 1, minor: 5, patch: 0 };
            const required = { major: 1, minor: 2, patch: 9 };
            assert.strictEqual(isVersionSufficient(actual, required), true);
        });

        test('should return false when actual minor is lower (same major)', () => {
            const actual = { major: 1, minor: 1, patch: 9 };
            const required = { major: 1, minor: 2, patch: 0 };
            assert.strictEqual(isVersionSufficient(actual, required), false);
        });

        test('should return true when actual patch is higher (same major.minor)', () => {
            const actual = { major: 1, minor: 2, patch: 5 };
            const required = { major: 1, minor: 2, patch: 3 };
            assert.strictEqual(isVersionSufficient(actual, required), true);
        });

        test('should return false when actual patch is lower (same major.minor)', () => {
            const actual = { major: 1, minor: 2, patch: 2 };
            const required = { major: 1, minor: 2, patch: 3 };
            assert.strictEqual(isVersionSufficient(actual, required), false);
        });
    });

    suite('buildGenerateCommand', () => {
        test('should build correct command with all parameters', () => {
            const result = buildGenerateCommand(
                'MyProject',
                'cs',
                'kafkaproducer',
                '/path/to/definitions.json',
                '/path/to/output'
            );
            
            assert.strictEqual(
                result,
                'xrcg generate --projectname MyProject --language cs --style kafkaproducer --definitions /path/to/definitions.json --output /path/to/output'
            );
        });

        test('should handle project names with special characters', () => {
            const result = buildGenerateCommand(
                'My-Project_v2',
                'java',
                'ehconsumer',
                'input.json',
                'output'
            );
            
            assert.ok(result.includes('--projectname My-Project_v2'));
        });

        test('should handle all supported languages', () => {
            const languages = ['cs', 'java', 'py', 'ts'];
            
            for (const lang of languages) {
                const result = buildGenerateCommand('Test', lang, 'kafkaproducer', 'in.json', 'out');
                assert.ok(result.includes(`--language ${lang}`));
            }
        });

        test('should handle various styles', () => {
            const styles = [
                'kafkaproducer', 'kafkaconsumer',
                'ehproducer', 'ehconsumer',
                'sbproducer', 'sbconsumer',
                'amqpproducer', 'amqpconsumer',
                'mqttclient', 'egproducer'
            ];
            
            for (const style of styles) {
                const result = buildGenerateCommand('Test', 'cs', style, 'in.json', 'out');
                assert.ok(result.includes(`--style ${style}`));
            }
        });
    });
});
