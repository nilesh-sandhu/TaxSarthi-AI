const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

// =====================================================
// TOKEN
// =====================================================

function getToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem("taxsarthi_token");
}

// =====================================================
// GENERIC REQUEST
// =====================================================

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    (headers as Record<string, string>).Authorization =
      `Bearer ${token}`;
  }

  const response = await fetch(
    `${API_BASE}${endpoint}`,
    {
      ...options,
      headers,
      cache: "no-store",
    }
  );

  if (!response.ok) {
    let message = "API request failed";

    try {
      const data = await response.json();

      message =
        data?.detail ||
        data?.message ||
        message;
    } catch {
      // Ignore JSON parsing errors
    }

    if (
      response.status === 401 &&
      typeof window !== "undefined"
    ) {
      localStorage.removeItem("taxsarthi_token");
      localStorage.removeItem("taxsarthi_user");
    }

    throw new Error(message);
  }

  return response.json();
}

// =====================================================
// AUTH
// =====================================================

export async function login(
  email: string,
  password: string
) {
  const result = await request<{
    access_token: string;
    token_type: string;
  }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (typeof window !== "undefined") {
    localStorage.setItem(
      "taxsarthi_token",
      result.access_token
    );
  }

  return result;
}

export async function googleLogin(
  credential: string
) {
  const result = await request<{
    access_token: string;
    token_type: string;
  }>("/auth/google", {
    method: "POST",
    body: JSON.stringify({
      credential,
    }),
  });

  if (typeof window !== "undefined") {
    localStorage.setItem(
      "taxsarthi_token",
      result.access_token
    );
  }

  return result;
}

export async function register(
  fullName: string,
  email: string,
  mobile: string,
  password: string
) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify({
      full_name: fullName,
      email,
      mobile,
      password,
    }),
  });
}

export async function getCurrentUser() {
  const user = await request<any>("/auth/me");

  if (typeof window !== "undefined") {
    localStorage.setItem(
      "taxsarthi_user",
      JSON.stringify(user)
    );
  }

  return user;
}

export function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("taxsarthi_token");
    localStorage.removeItem("taxsarthi_user");
  }
}

export function isLoggedIn(): boolean {
  if (typeof window === "undefined") {
    return false;
  }

  return !!localStorage.getItem("taxsarthi_token");
}

// =====================================================
// HEALTH
// =====================================================

export async function getHealth() {
  return request("/health/");
}

// =====================================================
// AI CHAT
// =====================================================

export async function askTaxSarthi(
  question: string
) {
  return request("/ai/chat", {
    method: "POST",
    body: JSON.stringify({
      question,
    }),
  });
}

// =====================================================
// CHAT HISTORY
// =====================================================

export interface ChatHistoryMessage {
  id: number;
  role: "user" | "assistant";
  message: string;
  created_at?: string | null;
}

export interface ChatHistoryResponse {
  success: boolean;
  user_id: number;
  total: number;
  history: ChatHistoryMessage[];
}

export async function getChatHistory(
  limit = 100
) {
  return request<ChatHistoryResponse>(
    `/chat/history?limit=${limit}`
  );
}

export async function clearChatHistory() {
  return request("/chat/history", {
    method: "DELETE",
  });
}

// =====================================================
// BUSINESS PROFILE
// =====================================================

export interface BusinessProfile {
  id: number;
  user_id: number;

  business_name: string;
  owner_name: string;
  business_type: string;
  state: string;
  turnover: number;

  gstin?: string | null;
  registration_type?: string | null;

  interstate: boolean;
  ecommerce: boolean;
  composition_scheme: boolean;

  business_status: string;
  is_active: boolean;

  created_at: string;
  updated_at: string;
}

export interface BusinessProfileCreate {
  business_name: string;
  owner_name: string;
  business_type: string;
  state: string;
  turnover: number;

  gstin?: string | null;
  registration_type?: string | null;

  interstate: boolean;
  ecommerce: boolean;
  composition_scheme: boolean;

  business_status: string;
}

export interface BusinessProfileUpdate {
  business_name?: string;
  owner_name?: string;
  business_type?: string;
  state?: string;
  turnover?: number;

  gstin?: string | null;
  registration_type?: string | null;

  interstate?: boolean;
  ecommerce?: boolean;
  composition_scheme?: boolean;

  business_status?: string;
  is_active?: boolean;
}

export async function getBusinessProfiles() {
  return request<BusinessProfile[]>(
    "/business-profiles/"
  );
}

export async function getBusinessProfile(
  businessId: number
) {
  return request<BusinessProfile>(
    `/business-profiles/${businessId}`
  );
}

export async function createBusinessProfile(
  profile: BusinessProfileCreate
) {
  return request<BusinessProfile>(
    "/business-profiles/",
    {
      method: "POST",
      body: JSON.stringify(profile),
    }
  );
}

export async function updateBusinessProfile(
  businessId: number,
  profile: BusinessProfileUpdate
) {
  return request<BusinessProfile>(
    `/business-profiles/${businessId}`,
    {
      method: "PUT",
      body: JSON.stringify(profile),
    }
  );
}

export async function deleteBusinessProfile(
  businessId: number
) {
  return request(
    `/business-profiles/${businessId}`,
    {
      method: "DELETE",
    }
  );
}

// =====================================================
// NOTIFICATIONS
// =====================================================

export async function getNotifications() {
  return request<any[]>("/notifications/");
}

export async function getNotification(
  id: number
) {
  return request(
    `/notifications/${id}`
  );
}

// =====================================================
// CIRCULARS
// =====================================================

export async function getCirculars() {
  return request<any[]>("/circulars/");
}

export async function searchCirculars(
  keyword: string
) {
  return request<any[]>(
    `/circulars/search/${encodeURIComponent(keyword)}`
  );
}

// =====================================================
// HSN
// =====================================================

export async function searchHSN(
  product: string
) {
  return request<any[]>(
    `/hsn/search/product/${encodeURIComponent(product)}`
  );
}

export async function searchHSNCode(
  code: string
) {
  return request<any[]>(
    `/hsn/search/code/${encodeURIComponent(code)}`
  );
}

// =====================================================
// PRODUCTS
// =====================================================

export async function searchProducts(
  keyword: string
) {
  return request<any[]>(
    `/products/search/${encodeURIComponent(keyword)}`
  );
}

// =====================================================
// UNIVERSAL SEARCH
// =====================================================

export async function universalSearch(
  query: string
) {
  return request(
    `/search/?q=${encodeURIComponent(query)}`
  );
}

// =====================================================
// GST CALCULATOR
// =====================================================

export async function calculateGST(
  amount: number,
  gstRate: number,
  calculationType: string,
  interstate = false
) {
  return request(
    "/calculator/",
    {
      method: "POST",
      body: JSON.stringify({
        amount,
        gst_rate: gstRate,
        calculation_type: calculationType,
        interstate,
      }),
    }
  );
}

// =====================================================
// DASHBOARD
// =====================================================

export async function getDashboard() {
  return request("/dashboard/");
}

// =====================================================
// REGISTRATION
// =====================================================

export async function checkRegistration(
  userId: number
) {
  return request(
    `/registration/check/${userId}`
  );
}

// =====================================================
// RETURNS
// =====================================================

export async function getReturns(
  registrationType: string
) {
  return request(
    "/returns/advisor",
    {
      method: "POST",
      body: JSON.stringify({
        registration_type: registrationType,
      }),
    }
  );
}