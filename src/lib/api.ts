export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface FactCheckResponse {
    CLAIM: string;
    TRUTH: string;
    EXPLAINATION: string;
    flagging: string;
    countering_misinformation: string;
    classifiers: string[];
    automated_fact_verification_pipeline: string[];
    credibility_scoring_mechanism: number;
    inconsistencies: string[];
    links: string[];
}

export async function verifyText(claim: string, language: string = "en"): Promise<FactCheckResponse> {
    const formData = new FormData();
    formData.append("claim", claim);
    formData.append("language", language);

    const response = await fetch(`${API_BASE_URL}/verify/text`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`Text verification failed: ${response.statusText}`);
    }

    return response.json();
}

export async function verifyMultimodal(file: File, language: string = "en"): Promise<FactCheckResponse> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("language", language);

    const response = await fetch(`${API_BASE_URL}/verify/multimodal`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`File verification failed: ${response.statusText}`);
    }

    return response.json();
}
