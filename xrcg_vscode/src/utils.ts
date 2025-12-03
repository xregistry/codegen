import * as path from 'path';

/**
 * Gets a suggested output path based on the input file path and a pattern.
 * The pattern can contain {input_file_name} which will be replaced with the input file's base name.
 * 
 * @param inputFilePath - The path to the input file
 * @param suggestedOutputPath - The suggested output path pattern
 * @returns The resolved output path
 */
export function getSuggestedOutputPath(inputFilePath: string, suggestedOutputPath: string): string {
    const inputFileName = inputFilePath ? path.basename(inputFilePath, path.extname(inputFilePath)) : '';
    const outFileName = suggestedOutputPath.replace('{input_file_name}', inputFileName);
    return path.join(path.dirname(inputFilePath), outFileName);
}

/**
 * Parses a version string and returns major, minor, patch components.
 * 
 * @param versionString - Version string like "0.9.0" or "xrcg version 0.9.0"
 * @returns Object with major, minor, patch or null if parsing fails
 */
export function parseVersion(versionString: string): { major: number; minor: number; patch: number } | null {
    const versionMatch = versionString.match(/(\d+)\.(\d+)\.(\d+)/);
    if (!versionMatch) {
        return null;
    }
    return {
        major: parseInt(versionMatch[1]),
        minor: parseInt(versionMatch[2]),
        patch: parseInt(versionMatch[3])
    };
}

/**
 * Compares two versions to check if the actual version is at least the required version.
 * 
 * @param actual - The actual version object
 * @param required - The required version object
 * @returns true if actual >= required
 */
export function isVersionSufficient(
    actual: { major: number; minor: number; patch: number },
    required: { major: number; minor: number; patch: number }
): boolean {
    if (actual.major > required.major) {
        return true;
    }
    if (actual.major < required.major) {
        return false;
    }
    // major versions are equal
    if (actual.minor > required.minor) {
        return true;
    }
    if (actual.minor < required.minor) {
        return false;
    }
    // minor versions are equal
    return actual.patch >= required.patch;
}

/**
 * Builds the xrcg generate command string.
 * 
 * @param projectName - The project name
 * @param language - The target language (cs, java, py, ts)
 * @param style - The generation style (kafkaproducer, ehconsumer, etc.)
 * @param definitionsPath - Path to the xRegistry definitions file
 * @param outputPath - Path to the output directory
 * @returns The complete command string
 */
export function buildGenerateCommand(
    projectName: string,
    language: string,
    style: string,
    definitionsPath: string,
    outputPath: string
): string {
    return `xrcg generate --projectname ${projectName} --language ${language} --style ${style} --definitions ${definitionsPath} --output ${outputPath}`;
}
