"use client";

import Link from "next/link";
import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  ArrowUp,
  Menu,
  Paperclip,
  Plus,
  Sun,
  Moon,
  MessageSquare,
  FileText,
  CheckCircle2,
  AlertTriangle,
  ShieldCheck,
  X,
} from "lucide-react";

import {
  askTaxSarthi,
  login as apiLogin,
  googleLogin,
  logout as apiLogout,
  getCurrentUser,
  isLoggedIn,
  getChatHistory,
  clearChatHistory,
  getBusinessProfiles,
  calculateGST,
  searchHSN,
  searchHSNCode,
  searchProducts,
  getReturns
} from "../lib/api";


type Message = {
  role: "user" | "assistant";
  content: string;
  analysis?: InvoiceAnalysis;
};

type CurrentUser = {
  id: number;
  full_name: string;
  email: string;
  mobile: string;
  role: string;
  created_at?: string;
};

type ChatHistoryItem = {
  id: number;
  role: "user" | "assistant";
  message: string;
  created_at?: string | null;
};


type InvoiceAnalysis = {
  success?: boolean;
  invoice?: Record<string, any>;
  validation?: Record<string, any>;
  risk?: Record<string, any>;
  fraud?: Record<string, any>;
  duplicates?: any[];
  recommendations?: any[];
  summary?: Record<string, any>;
};


type UploadedFile = {
  name: string;
  status: "uploading" | "success" | "error";
  analysis?: InvoiceAnalysis;
  error?: string;
};



function InvoiceAnalysisCard({
  analysis,
}: {
  analysis: InvoiceAnalysis;
}) {
  const summary = analysis.summary ?? {};
  const invoice = analysis.invoice ?? {};
  const validation = analysis.validation ?? {};
  const risk = analysis.risk ?? {};
  const fraud = analysis.fraud ?? {};

  const getValue = (...values: any[]) => {
    const found = values.find(
      (value) =>
        value !== undefined &&
        value !== null &&
        value !== ""
    );

    return found ?? "Not available";
  };

  const invoiceNumber = getValue(
    summary.invoice_number,
    invoice.invoice_number
  );

  const invoiceDate = getValue(
    summary.invoice_date,
    invoice.invoice_date
  );

  const supplier = getValue(
    summary.supplier,
    invoice.supplier
  );

  const buyer = getValue(
    summary.buyer,
    invoice.buyer
  );

  const supplierGstin = getValue(
    summary.supplier_gstin,
    invoice.supplier_gstin
  );

  const buyerGstin = getValue(
    summary.buyer_gstin,
    invoice.buyer_gstin
  );

  const taxableAmount = getValue(
    summary.taxable_amount,
    invoice.taxable_amount
  );

  const cgst = getValue(
    summary.cgst,
    invoice.cgst
  );

  const sgst = getValue(
    summary.sgst,
    invoice.sgst
  );

  const igst = getValue(
    summary.igst,
    invoice.igst
  );

  const totalAmount = getValue(
    summary.total_amount,
    invoice.total_amount
  );

  const riskScore = getValue(
    risk.score,
    risk.risk_score,
    risk.total_score
  );

  const riskLevel = getValue(
    risk.level,
    risk.risk_level,
    risk.status
  );

  const duplicateCount =
    summary.duplicate_count ??
    analysis.duplicates?.length ??
    0;

  const fraudCount =
    summary.fraud_count ??
    (Array.isArray(fraud)
      ? fraud.length
      : Object.keys(fraud).length);

  const validationErrors =
    Array.isArray(validation.errors)
      ? validation.errors
      : [];

  const recommendations =
    Array.isArray(analysis.recommendations)
      ? analysis.recommendations
      : [];

  const isValid =
    validation.valid === true ||
    String(
      validation.status ?? ""
    ).toLowerCase() === "valid";

  return (
    <div className="invoice-analysis-card">

      <div className="invoice-card-header">
        <div>
          <span className="invoice-card-label">
            Invoice Analysis
          </span>

          <h3>
            Analysis completed
          </h3>
        </div>

        <div
          className={
            isValid
              ? "invoice-status valid"
              : "invoice-status review"
          }
        >
          {isValid ? (
            <CheckCircle2 size={16} />
          ) : (
            <AlertTriangle size={16} />
          )}

          {isValid ? "Valid" : "Review"}
        </div>
      </div>


      <div className="invoice-details-grid">

        <div className="invoice-detail">
          <span>Invoice Number</span>
          <strong>{invoiceNumber}</strong>
        </div>

        <div className="invoice-detail">
          <span>Invoice Date</span>
          <strong>{invoiceDate}</strong>
        </div>

        <div className="invoice-detail">
          <span>Supplier</span>
          <strong>{supplier}</strong>
        </div>

        <div className="invoice-detail">
          <span>Buyer</span>
          <strong>{buyer}</strong>
        </div>

        <div className="invoice-detail">
          <span>Supplier GSTIN</span>
          <strong>{supplierGstin}</strong>
        </div>

        <div className="invoice-detail">
          <span>Buyer GSTIN</span>
          <strong>{buyerGstin}</strong>
        </div>

      </div>


      <div className="invoice-amounts">

        <div>
          <span>Taxable Amount</span>
          <strong>{taxableAmount}</strong>
        </div>

        <div>
          <span>CGST</span>
          <strong>{cgst}</strong>
        </div>

        <div>
          <span>SGST</span>
          <strong>{sgst}</strong>
        </div>

        <div>
          <span>IGST</span>
          <strong>{igst}</strong>
        </div>

        <div className="invoice-total">
          <span>Total Amount</span>
          <strong>{totalAmount}</strong>
        </div>

      </div>


      <div className="invoice-checks">

        <div className="invoice-check">
          <CheckCircle2 size={17} />
          <span>Validation</span>
          <strong>
            {isValid ? "Valid" : "Review"}
          </strong>
        </div>

        <div className="invoice-check">
          <ShieldCheck size={17} />
          <span>Fraud Indicators</span>
          <strong>{fraudCount}</strong>
        </div>

        <div className="invoice-check">
          <FileText size={17} />
          <span>Duplicate Matches</span>
          <strong>{duplicateCount}</strong>
        </div>

      </div>


      <div className="invoice-risk">

        <div>
          <span>Risk Score</span>
          <strong>{riskScore}</strong>
        </div>

        <div>
          <span>Risk Level</span>
          <strong>{riskLevel}</strong>
        </div>

      </div>


      {validationErrors.length > 0 && (

        <div className="invoice-validation-errors">

          <div className="invoice-section-title">
            Validation Issues
          </div>

          {validationErrors.map(
            (error: any, index: number) => (
              <div
                key={index}
                className="invoice-error-item"
              >
                {typeof error === "string"
                  ? error
                  : error?.message ??
                    JSON.stringify(error)}
              </div>
            )
          )}

        </div>

      )}


      {recommendations.length > 0 && (

        <div className="invoice-recommendations">

          <div className="invoice-section-title">
            Recommendations
          </div>

          <ul>
            {recommendations.map(
              (item: any, index: number) => (
                <li key={index}>
                  {typeof item === "string"
                    ? item
                    : item?.message ??
                      item?.recommendation ??
                      JSON.stringify(item)}
                </li>
              )
            )}
          </ul>

        </div>

      )}

    </div>
  );
}


export default function Home() {

  const [dark, setDark] = useState(true);

  const [message, setMessage] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [uploadedFile, setUploadedFile] =
    useState<UploadedFile | null>(null);

  const [currentUser, setCurrentUser] =
    useState<CurrentUser | null>(null);
  const [loginOpen, setLoginOpen] = useState(false);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState("");
  const [history, setHistory] = useState<ChatHistoryItem[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  const fileInputRef =
    useRef<HTMLInputElement | null>(null);

  const messagesEndRef =
    useRef<HTMLDivElement | null>(null);


  // =====================================================
  // AUTO SCROLL
  // =====================================================

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading, uploadedFile]);


  useEffect(() => {
    let mounted = true;
    const initializeAuth = async () => {
      if (!isLoggedIn()) return;
      try {
        const user = await getCurrentUser();
        if (!mounted) return;
        setCurrentUser(user as CurrentUser);
        setHistoryLoading(true);
        const result = await getChatHistory(100);
        if (mounted) setHistory(Array.isArray(result?.history) ? result.history : []);
      } catch (error) {
        console.error("Authentication initialization error:", error);
        apiLogout();
        if (mounted) { setCurrentUser(null); setHistory([]); }
      } finally {
        if (mounted) setHistoryLoading(false);
      }
    };
    initializeAuth();
    return () => { mounted = false; };
  }, []);

  // =====================================================
  // GOOGLE SIGN-IN
  // Initialize Google Identity Services only once.
  // =====================================================

  useEffect(() => {
    let cancelled = false;

    const initializeGoogle = () => {
      if (cancelled) return;

      const clientId =
        process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

      if (!clientId) {
        console.error(
          "NEXT_PUBLIC_GOOGLE_CLIENT_ID is missing."
        );
        return;
      }

      const google = (window as any).google;

      if (!google?.accounts?.id) {
        return;
      }

      const container =
        document.getElementById("google-login-button");

      if (!container || container.dataset.initialized === "true") {
        return;
      }

      google.accounts.id.initialize({
        client_id: clientId,
        callback: async (response: {
          credential?: string;
        }) => {
          if (!response.credential) {
            setLoginError(
              "Google did not return a valid credential."
            );
            return;
          }

          await handleGoogleLogin(
            response.credential
          );
        },
        auto_select: false,
        cancel_on_tap_outside: true,
      });

      container.innerHTML = "";

      google.accounts.id.renderButton(
        container,
        {
          type: "standard",
          theme: "outline",
          size: "large",
          text: "signin_with",
          shape: "rectangular",
          logo_alignment: "left",
          width: 320,
        }
      );

      container.dataset.initialized = "true";
    };

    const timer = window.setInterval(() => {
      initializeGoogle();

      const container =
        document.getElementById("google-login-button");

      if (container?.dataset.initialized === "true") {
        window.clearInterval(timer);
      }
    }, 300);

    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, []);

  const handleLogin = async (event?: React.FormEvent) => {
    event?.preventDefault();
    const email = loginEmail.trim();
    if (!email || !loginPassword) {
      setLoginError("Please enter your email and password.");
      return;
    }
    setLoginLoading(true);
    setLoginError("");
    try {
      await apiLogin(email, loginPassword);
      const user = await getCurrentUser();
      setCurrentUser(user as CurrentUser);
      const result = await getChatHistory(100);
      setHistory(Array.isArray(result?.history) ? result.history : []);
      setLoginEmail("");
      setLoginPassword("");
      setLoginOpen(false);
    } catch (error) {
      setLoginError(error instanceof Error ? error.message : "Login failed. Please check your credentials.");
    } finally {
      setLoginLoading(false);
    }
  };

  const handleGoogleLogin = async (
    credential: string
  ) => {
    setLoginLoading(true);
    setLoginError("");

    try {
      await googleLogin(credential);

      const user = await getCurrentUser();
      setCurrentUser(user as CurrentUser);

      const result = await getChatHistory(100);
      setHistory(
        Array.isArray(result?.history)
          ? result.history
          : []
      );

      setLoginOpen(false);
      setLoginEmail("");
      setLoginPassword("");
    } catch (error) {
      setLoginError(
        error instanceof Error
          ? error.message
          : "Google login failed."
      );
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLogout = () => {
    apiLogout();
    setCurrentUser(null);
    setHistory([]);
    setMessages([]);
    setMessage("");
    setUploadedFile(null);
  };


  // =====================================================
  // CLEAN AI RESPONSE
  // =====================================================

  const cleanResponse = (
    value: unknown
  ): string => {

    if (
      value === null ||
      value === undefined
    ) {
      return "No response received.";
    }

    if (
      typeof value !== "string"
    ) {
      return String(value);
    }

    return value
      .replace(/^#{1,6}\s*/gm, "")
      .replace(/\*\*(.*?)\*\*/g, "$1")
      .replace(/\*(.*?)\*/g, "$1")
      .replace(/__(.*?)__/g, "$1")
      .replace(
        /\[([^\]]+)\]\([^)]+\)/g,
        "$1"
      )
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  };


  // =====================================================
  // SEND AI MESSAGE
  // =====================================================

  // =====================================================
  // BUSINESS PROFILE RESPONSE
  // Frontend-only personalization for business questions.
  // Keeps backend unchanged.
  // =====================================================

  const isBusinessQuestion = (value: string): boolean => {
    const q = value.toLowerCase().trim();

    const patterns = [
      "my business",
      "about my business",
      "tell me about my business",
      "what do you know about my business",
      "business ke bare",
      "business ke baare",
      "mere business",
      "mera business",
      "my company",
      "business profile",
    ];

    return patterns.some((pattern) => q.includes(pattern));
  };

  const buildBusinessResponse = (business: any): string => {
    const businessName =
      business?.business_name || "Not available";

    const ownerName =
      business?.owner_name || "Not available";

    const businessType =
      business?.business_type || "Not available";

    const state =
      business?.state || "Not available";

    const turnover = Number(
      business?.turnover ?? 0
    );

    const gstRegistered = Boolean(
      business?.gstin &&
      String(business.gstin).trim()
    );

    const registrationType =
      business?.registration_type ||
      "Not specified";

    const interstate = Boolean(
      business?.interstate
    );

    const ecommerce = Boolean(
      business?.ecommerce
    );

    const composition = Boolean(
      business?.composition_scheme
    );

    const status =
      business?.business_status || "Active";

    const turnoverText =
      Number.isFinite(turnover)
        ? `₹${turnover.toLocaleString("en-IN")}`
        : "Not available";

    const gstStatus = gstRegistered
      ? `Registered${
          business?.gstin
            ? ` (GSTIN: ${business.gstin})`
            : ""
        }`
      : "Not Registered";

    const businessSize =
      turnover < 2000000
        ? "Micro"
        : turnover < 50000000
          ? "Small"
          : turnover < 250000000
            ? "Medium"
            : "Large";

    const riskReasons: string[] = [];

    if (interstate) {
      riskReasons.push(
        "Inter-State supplies are marked as applicable."
      );
    }

    if (ecommerce) {
      riskReasons.push(
        "E-commerce activity is marked as applicable."
      );
    }

    if (
      turnover > 4000000 &&
      !gstRegistered
    ) {
      riskReasons.push(
        "Turnover is above ₹40 lakh while GSTIN is not recorded."
      );
    }

    let riskLevel = "Low";

    if (riskReasons.length >= 2) {
      riskLevel = "High";
    } else if (riskReasons.length === 1) {
      riskLevel = "Medium";
    }

    const complianceScore = Math.max(
      0,
      100
        - (gstRegistered ? 0 : 30)
        - (
            turnover >= 4000000 &&
            !gstRegistered
              ? 40
              : 0
          )
        - (interstate ? 10 : 0)
        - (ecommerce ? 10 : 0)
    );

    const recommendations: string[] = [];

    if (!gstRegistered) {
      recommendations.push(
        "Review GST registration applicability for your actual supplies."
      );
    }

    if (interstate) {
      recommendations.push(
        "Review the GST implications of your inter-State outward supplies."
      );
    }

    if (ecommerce) {
      recommendations.push(
        "Review e-commerce GST obligations and applicable registration rules."
      );
    }

    recommendations.push(
      "Keep sales, purchase and tax records updated."
    );

    return [
      "Here is your TaxSarthi business analysis:",
      "",
      `Business Name: ${businessName}`,
      `Owner: ${ownerName}`,
      `Business Type: ${businessType}`,
      `State: ${state}`,
      `Annual Turnover: ${turnoverText}`,
      `Business Size: ${businessSize}`,
      `GST Status: ${gstStatus}`,
      `Registration Type: ${registrationType}`,
      `Inter-State Supply: ${
        interstate ? "Yes" : "No"
      }`,
      `E-commerce: ${
        ecommerce ? "Yes" : "No"
      }`,
      `Composition Scheme: ${
        composition ? "Yes" : "No"
      }`,
      `Business Status: ${status}`,
      "",
      "Compliance Snapshot:",
      `Risk Level: ${riskLevel}`,
      `Compliance Score: ${complianceScore}/100`,
      "",
      "Why this assessment:",
      ...(riskReasons.length > 0
        ? riskReasons.map(
            (item) => `• ${item}`
          )
        : [
            "• No major risk trigger was identified from the available profile fields."
          ]),
      "",
      "Recommended next steps:",
      ...recommendations.map(
        (item, index) =>
          `${index + 1}. ${item}`
      ),
      "",
      "Note: GST applicability depends on the actual nature of supplies and current law. Use the official GST portal for final filing and verification.",
    ].join("\n");
  };

  const parseGSTCalculationRequest = (
    value: string
  ): {
    amount: number;
    rate: number;
    type: string;
    interstate: boolean;
  } | null => {
    const q = value.toLowerCase();

    const isCalculation =
      /(?:calculate|calculation|compute|find|work out|gst on|tax on)/i.test(
        q
      ) &&
      /(?:gst|cgst|sgst|igst|tax)/i.test(
        q
      );

    if (!isCalculation) {
      return null;
    }

    const numbers =
      q.match(/\d+(?:\.\d+)?/g);

    if (!numbers || numbers.length < 2) {
      return null;
    }

    const amount = Number(numbers[0]);
    const rate = Number(numbers[1]);

    if (
      !Number.isFinite(amount) ||
      !Number.isFinite(rate) ||
      amount < 0 ||
      rate < 0
    ) {
      return null;
    }

    const interstate =
      /inter[- ]?state|igst|outside state|another state/i.test(
        q
      );

    const type =
      /inclusive|including gst|with gst/i.test(
        q
      )
        ? "inclusive"
        : "exclusive";

    return {
      amount,
      rate,
      type,
      interstate,
    };
  };

  const buildGSTCalculationResponse = (
    result: any,
    input: {
      amount: number;
      rate: number;
      type: string;
      interstate: boolean;
    }
  ): string => {
    const money = (value: unknown) => {
      const number = Number(value ?? 0);

      return `₹${
        Number.isFinite(number)
          ? number.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })
          : "0.00"
      }`;
    };

    return [
      "GST Calculation:",
      "",
      `Input Amount: ${money(input.amount)}`,
      `GST Rate: ${input.rate}%`,
      `Calculation Type: ${
        input.type === "inclusive"
          ? "GST Inclusive"
          : "GST Exclusive"
      }`,
      `Transaction Type: ${
        input.interstate
          ? "Inter-State (IGST)"
          : "Intra-State (CGST + SGST)"
      }`,
      "",
      "Result:",
      `Taxable Value: ${money(
        result?.taxable_value
      )}`,
      `GST Amount: ${money(
        result?.gst_amount
      )}`,
      `CGST: ${money(result?.cgst)}`,
      `SGST: ${money(result?.sgst)}`,
      `IGST: ${money(result?.igst)}`,
      `Total Invoice Value: ${money(
        result?.total_invoice_value
      )}`,
      "",
      "Official GST Portal: https://www.gst.gov.in/",
    ].join("\n");
  };


  // =====================================================
  // GST TOOL ROUTING
  // Uses existing backend endpoints plus a small curated FAQ layer for core GST questions.
  // =====================================================

  const detectGSTToolRequest = (
    value: string
  ) => {
    const q = value.toLowerCase().trim();

    const asksHSN =
      /\b(hsn|sac|hsn code|sac code)\b/i.test(q);

    const asksProductGST =
      /\b(gst on|gst rate on|tax rate on|gst for|rate for)\b/i.test(q);

    const asksReturn =
      /\b(gstr-?1|gstr-?3b|gstr-?9|gstr|gst return|returns|return filing|file return)\b/i.test(q);

    const asksITC =
      /\b(itc|input tax credit|input tax)\b/i.test(q);

    const asksRegistration =
      /\b(gst registration|register for gst|gstin|new gst registration|gst registration process)\b/i.test(q);

    const asksInvoice =
      /\b(invoice|tax invoice|bill|credit note|debit note|e-?invoice)\b/i.test(q);

    const asksEWy =
      /\b(e-?way bill|eway bill|way bill)\b/i.test(q);

    return {
      asksHSN,
      asksProductGST,
      asksReturn,
      asksITC,
      asksRegistration,
      asksInvoice,
      asksEWy,
    };
  };

  const extractSearchTerm = (
    value: string
  ): string => {
    return value
      .replace(
        /\b(what is|what's|tell me|give me|find|search|show me|gst on|gst rate on|gst for|rate for|hsn for|hsn code for|sac for)\b/gi,
        ""
      )
      .replace(/[?.,!]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  };

  const buildHSNResponse = (
    results: any[],
    productQuery: string
  ): string => {
    if (!results.length) {
      return [
        `I could not find an exact HSN/SAC match for "${productQuery}".`,
        "",
        "Please provide more product/service details such as product name, material, use, or service type so TaxSarthi can narrow the classification.",
        "",
        "For final classification, verify the applicable tariff/notification before issuing an invoice.",
      ].join("\n");
    }

    const lines = [
      `HSN/SAC results for "${productQuery}":`,
      "",
    ];

    results.slice(0, 8).forEach(
      (item, index) => {
        lines.push(
          `${index + 1}. HSN/SAC: ${
            item?.hsn_code ??
            item?.sac_code ??
            item?.code ??
            "Not available"
          }`
        );

        if (item?.description) {
          lines.push(
            `   Description: ${item.description}`
          );
        }

        if (
          item?.gst_rate !== undefined &&
          item?.gst_rate !== null
        ) {
          lines.push(
            `   GST Rate: ${item.gst_rate}%`
          );
        }

        if (item?.category) {
          lines.push(
            `   Category: ${item.category}`
          );
        }

        lines.push("");
      }
    );

    lines.push(
      "Tip: HSN/SAC classification should be confirmed against the exact nature of the goods/services before invoicing."
    );

    return lines.join("\n");
  };

  const buildProductResponse = (
    results: any[],
    productQuery: string
  ): string => {
    if (!results.length) {
      return [
        `I could not find a product match for "${productQuery}".`,
        "",
        "Try the exact product name, brand/category, or ask for its HSN/GST rate with more details.",
      ].join("\n");
    }

    const lines = [
      `GST/product information for "${productQuery}":`,
      "",
    ];

    results.slice(0, 8).forEach(
      (item, index) => {
        lines.push(
          `${index + 1}. ${
            item?.name ??
            item?.product_name ??
            item?.description ??
            productQuery
          }`
        );

        if (item?.gst_rate !== undefined) {
          lines.push(
            `   GST Rate: ${item.gst_rate}%`
          );
        } else if (item?.gst !== undefined) {
          lines.push(
            `   GST Rate: ${item.gst}%`
          );
        }

        if (
          item?.hsn_code ||
          item?.hsn
        ) {
          lines.push(
            `   HSN: ${
              item.hsn_code ??
              item.hsn
            }`
          );
        }

        if (item?.category) {
          lines.push(
            `   Category: ${item.category}`
          );
        }

        lines.push("");
      }
    );

    lines.push(
      "Verify the exact classification and rate for the specific product description and applicable period before invoicing."
    );

    return lines.join("\n");
  };

  const buildReturnsResponse = (
    result: any,
    registrationType: string
  ): string => {
    if (!result) {
      return [
        "I could not retrieve the return guidance right now.",
        "",
        `Registration type provided: ${registrationType || "not specified"}.`,
        "Please check the GST portal for the applicable return forms and filing status.",
      ].join("\n");
    }

    const lines = [
      "GST Return Guidance:",
      "",
      `Registration Type: ${registrationType || "Not specified"}`,
    ];

    if (typeof result === "string") {
      lines.push("", result);
    } else {
      for (const [key, value] of Object.entries(
        result as Record<string, unknown>
      )) {
        if (
          value !== null &&
          value !== undefined &&
          value !== ""
        ) {
          const label = key
            .replace(/_/g, " ")
            .replace(/\b\w/g, (c) =>
              c.toUpperCase()
            );

          lines.push(
            `${label}: ${
              typeof value === "object"
                ? JSON.stringify(value)
                : String(value)
            }`
          );
        }
      }
    }

    lines.push(
      "",
      "Returns depend on your taxpayer type, registration status, turnover, and activities. Verify the applicable due date and form on the GST portal before filing."
    );

    return lines.join("\n");
  };

  const buildITCResponse = (
    originalAnswer: string
  ): string => {
    return [
      originalAnswer,
      "",
      "ITC checklist:",
      "• Check that the purchase is eligible for input tax credit.",
      "• Keep a valid tax invoice or prescribed supporting document.",
      "• Confirm the supplier-side reporting/credit availability where applicable.",
      "• Reconcile purchase records with the relevant GST data before claiming credit.",
      "• Check blocked-credit rules and other conditions for the specific expense.",
      "",
      "For a transaction-specific ITC decision, share the purchase type, invoice details, GST registration status, and business use.",
    ].join("\n");
  };

  // =====================================================
  // CORE GST FAQ MODE
  // Fast, deterministic answers for common GST questions.
  // Dynamic product/HSN/calculation requests continue to
  // use the existing backend tools.
  // =====================================================

  const getFixedGSTAnswer = (value: string): string | null => {
    const q = value.toLowerCase().replace(/[?!.,]/g, " ").replace(/\s+/g, " ").trim();
    const portal = "Official GST Portal: https://www.gst.gov.in/";
    const cbic = "Official CBIC GST information: https://cbic-gst.gov.in/";
    const notifications = "Official GST notifications: https://cbic-gst.gov.in/hindi/central-tax-notifications.html";
    const einvoice = "Official e-Invoice portal: https://einvoice.gst.gov.in/";
    const any = (...terms: string[]) => terms.some((t) => q.includes(t));
    const exact = (...terms: string[]) => terms.includes(q);

    if (exact("hi", "hello", "hey", "hii", "helo", "namaste"))
      return "Hello! Im TaxSarthi AI. Ask me about GST, GST registration, GST rates, HSN/SAC, ITC, returns, invoices, e-invoicing, e-way bills, refunds, compliance or notificationns"



    if (exact("gst") || any("what is gst", "what's gst", "define gst", "gst kya hai", "gst kya hota hai", "gst meaning", "meaning of gst"))
      return `GST (Goods and Services Tax) is a destination-based indirect tax on the supply of goods and services in India. It taxes value addition through the supply chain, subject to the GST law.

Main components:
• CGST — Central GST
• SGST/UTGST — State/Union Territory GST
• IGST — Integrated GST, generally for inter-State supplies

${portal}
${cbic}`;

    if (any("gstin", "what is gstin", "gst number", "gst registration number", "gstin kya hai"))
      return `GSTIN is the Goods and Services Tax Identification Number allotted to a registered taxpayer. It is used for GST identification, invoicing, returns and compliance.

GSTINs can also be checked through the GST Portal Search Taxpayer facility.

${portal}`;

    if (any("what is hsn", "hsn kya hai", "hsn meaning", "hsn code kya hai"))
      return "HSN (Harmonized System of Nomenclature) classifies goods for GST/tax reporting and invoicing. The correct HSN depends on the exact product and classification. Ask “HSN for laptop” or “HSN for shirt” for a product lookup.";

    if (any("what is sac", "sac kya hai", "sac code", "sac meaning"))
      return "SAC (Services Accounting Code) is used to classify services for GST. The correct SAC depends on the exact service being supplied.";

    if (any("what is itc", "itc kya hai", "input tax credit", "what is input tax credit", "input tax kya hai"))
      return "ITC (Input Tax Credit) is eligible GST credit for GST paid on qualifying business purchases, subject to applicable conditions and restrictions. Check the invoice/document, business use, reconciliation, supplier/reporting availability where applicable and blocked-credit rules.";

    if (any("how does itc work", "how to claim itc", "can i claim itc", "itc claim kaise"))
      return "To claim ITC, the purchase must satisfy the applicable GST conditions and be supported by the required documents. Reconcile purchase records with relevant GST data and check blocked-credit rules. ITC eligibility is transaction-specific.";

    if (exact("cgst", "sgst", "igst") || any("what is cgst", "what is sgst", "what is igst", "cgst vs sgst", "cgst and sgst", "igst vs cgst", "cgst kya hai", "sgst kya hai", "igst kya hai"))
      return "CGST is the Central GST component and SGST/UTGST is the State/UT component generally charged together on eligible intra-State supplies. IGST is generally used for inter-State supplies. Example: an applicable 18% intra-State supply may have 9% CGST + 9% SGST; an applicable 18% inter-State supply generally has 18% IGST.";

    if (any("gst registration", "register for gst", "how to register for gst", "gst registration process", "gst registration kya hai", "gstin kaise", "new gst registration"))
      return `GST registration is the process of obtaining GST registration and, after approval, a GSTIN. Basic process: check applicability, open the GST Portal, enter PAN/business/contact/identity details, complete verification, submit the application and complete any clarification/verification requested.

${portal}`;

    if (any("who needs gst registration", "is gst registration mandatory", "gst registration compulsory"))
      return "GST registration is not decided by turnover alone. Turnover thresholds, nature of supply, inter-State supplies, e-commerce and other compulsory-registration provisions can affect applicability. Share your State, turnover, business type and supply pattern for a business-specific assessment.";

    if (any("what is gstr 1", "what is gstr1", "gstr 1 kya hai", "gstr1 kya hai"))
      return "GSTR-1 is used by applicable taxpayers to report outward-supply details. Exact tables, filing frequency and applicability depend on the taxpayer and applicable scheme.";

    if (any("what is gstr 3b", "what is gstr3b", "gstr 3b kya hai", "gstr3b kya hai"))
      return "GSTR-3B is a summary GST return used by applicable taxpayers to report supply/tax information, eligible ITC and tax liability/payment. Exact requirements depend on the taxpayer and applicable rules.";

    if (any("what is gstr 9", "what is gstr9", "gstr 9 kya hai", "annual gst return"))
      return "GSTR-9 is an annual GST return for applicable taxpayers, subject to the exemptions and conditions for the relevant financial year. It consolidates relevant GST information for that year.";

    if (any("gst return", "gst returns", "which gst return", "which return should i file", "return filing", "gst filing"))
      return "Common GST returns/forms include GSTR-1 for outward supplies, GSTR-3B for summary tax/ITC reporting and payment, and GSTR-9 as an annual return for applicable taxpayers. The correct form and frequency depend on registration type, activity and scheme.";

    if (any("what is e invoice", "what is e-invoice", "e invoice kya hai", "einvoice kya hai"))
      return `e-Invoicing means reporting specified GST documents to an Invoice Registration Portal (IRP) and obtaining an Invoice Reference Number (IRN). It does not mean the government creates your ordinary invoice. Applicable reported invoices can receive an IRN and QR code.

${einvoice}`;

    if (any("what is e way bill", "what is e-way bill", "eway bill kya hai", "e way bill kya hai"))
      return `An e-Way Bill is an electronic document for movement of goods when applicable GST rules require it. Applicability depends on the nature/value of movement and prescribed exceptions.

${portal}`;

    if (any("composition scheme", "what is composition", "composition scheme kya hai"))
      return "The Composition Scheme is a simplified GST scheme available only to eligible taxpayers subject to prescribed conditions and restrictions. Eligibility depends on turnover, business type and supply pattern.";

    if (any("gst invoice", "tax invoice", "gst bill", "invoice under gst", "what should be on gst invoice"))
      return "A GST tax invoice generally contains supplier/recipient details, invoice number/date, description, HSN/SAC where applicable, taxable value, GST rate and tax amounts, plus other prescribed particulars. If e-invoicing applies, prescribed IRN/QR requirements also need to be followed.";

    if (any("credit note", "credit note kya hai"))
      return "A credit note is issued in specified GST-law situations such as permitted reductions/adjustments to the value or tax of an earlier supply. Reporting and tax adjustment must follow applicable GST provisions.";

    if (any("debit note", "debit note kya hai"))
      return "A debit note is used in specified situations where additional taxable value or tax becomes payable in relation to an earlier supply, subject to applicable GST rules and reporting requirements.";

    if (any("gst refund", "refund under gst", "gst refund kya hai", "how to claim gst refund"))
      return `A GST refund is a refund of eligible tax/amounts under prescribed GST provisions. Eligibility, documents, form and time limit depend on the reason for refund.

${portal}`;

    if (any("reverse charge", "rcm", "reverse charge mechanism", "rcm kya hai"))
      return "Reverse Charge Mechanism (RCM) means the recipient is liable to pay GST instead of the supplier in specified cases. Whether RCM applies depends on the exact transaction and applicable provisions.";

    if (any("place of supply", "place of supply kya hai", "pos under gst"))
      return "Place of Supply rules determine the location of a supply for GST purposes. They help decide whether a transaction is intra-State or inter-State and therefore which GST component applies.";

    if (any("gst compliance", "compliance kya hai", "gst compliance kya hai"))
      return "GST compliance includes applicable registration, invoicing, records, return filing, tax payment, ITC reconciliation and other prescribed obligations. The exact checklist depends on the business and registration type.";

    if (any("latest notification", "latest gst notification", "gst notification", "gst notifications", "gst circular", "latest gst circular", "notification detail", "notification details"))
      return `GST notifications and circulars can change rates, procedures and compliance requirements. For the current official notification list:
${notifications}

For general GST services and taxpayer functions:
${portal}

For CBIC GST information:
${cbic}

If you give me a notification number or topic, I can explain its subject and practical impact when the relevant data is available.`;

    if (any("gst rate", "gst rates", "what is gst rate", "gst rate kya hai"))
      return "GST rates vary by the classification and nature of goods/services and applicable notifications/conditions. Give me the exact product or service and TaxSarthi can search the available GST/HSN information.";

    if (any("gst notice", "gst notice kya hai", "i received a gst notice"))
      return "A GST notice is a communication from tax authorities seeking information, clarification, payment, compliance or other action. Check the notice number, section, issue, period and response deadline carefully. You can upload the notice here and TaxSarthi can explain it.";

    return null;
  };

  const sendMessage = async (text?: string) => {
    const userMessage = (text ?? message).trim();
    if (!userMessage || loading) return;

    setMessage("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const fixedAnswer =
        getFixedGSTAnswer(userMessage);

      if (fixedAnswer) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: fixedAnswer },
        ]);
        if (currentUser) {
          try {
            const h = await getChatHistory(100);
            setHistory(Array.isArray(h?.history) ? h.history : []);
          } catch {}
        }
        return;
      }

      const toolRequest =
        detectGSTToolRequest(userMessage);

      const calculation =
        parseGSTCalculationRequest(
          userMessage
        );

      if (calculation) {
        try {
          const result =
            await calculateGST(
              calculation.amount,
              calculation.rate,
              calculation.type,
              calculation.interstate
            );

          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content:
                buildGSTCalculationResponse(
                  result,
                  calculation
                ),
            },
          ]);

          if (currentUser) {
            try {
              const historyResult =
                await getChatHistory(100);

              setHistory(
                Array.isArray(
                  historyResult?.history
                )
                  ? historyResult.history
                  : []
              );
            } catch (historyError) {
              console.warn(
                "Could not refresh chat history:",
                historyError
              );
            }
          }

          return;
        } catch (calculationError) {
          console.error(
            "GST calculation error:",
            calculationError
          );
          // Fall through to the normal AI response
          // if the calculation endpoint is unavailable.
        }
      }


      // -------------------------------------------------
      // HSN / SAC lookup
      // -------------------------------------------------
      if (
        toolRequest.asksHSN
      ) {
        try {
          const term =
            extractSearchTerm(
              userMessage
            );

          const results =
            await searchHSN(term);

          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content:
                buildHSNResponse(
                  Array.isArray(results)
                    ? results
                    : [],
                  term
                ),
            },
          ]);

          if (currentUser) {
            try {
              const h =
                await getChatHistory(100);
              setHistory(
                Array.isArray(h?.history)
                  ? h.history
                  : []
              );
            } catch {}
          }

          return;
        } catch (toolError) {
          console.warn(
            "HSN search failed; falling back to AI.",
            toolError
          );
        }
      }

      // -------------------------------------------------
      // Product GST lookup
      // -------------------------------------------------
      if (
        toolRequest.asksProductGST &&
        !toolRequest.asksHSN &&
        !/(?:calculate|calculation|compute|work out)/i.test(userMessage)
      ) {
        try {
          const term =
            extractSearchTerm(
              userMessage
            );

          const results =
            await searchProducts(term);

          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content:
                buildProductResponse(
                  Array.isArray(results)
                    ? results
                    : [],
                  term
                ),
            },
          ]);

          if (currentUser) {
            try {
              const h =
                await getChatHistory(100);
              setHistory(
                Array.isArray(h?.history)
                  ? h.history
                  : []
              );
            } catch {}
          }

          return;
        } catch (toolError) {
          console.warn(
            "Product search failed; falling back to AI.",
            toolError
          );
        }
      }

      // -------------------------------------------------
      // GST returns
      // -------------------------------------------------
      if (
        toolRequest.asksReturn
      ) {
        try {
          const registrationType =
            "regular";

          const result =
            await getReturns(
              registrationType
            );

          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content:
                buildReturnsResponse(
                  result,
                  registrationType
                ),
            },
          ]);

          if (currentUser) {
            try {
              const h =
                await getChatHistory(100);
              setHistory(
                Array.isArray(h?.history)
                  ? h.history
                  : []
              );
            } catch {}
          }

          return;
        } catch (toolError) {
          console.warn(
            "Returns lookup failed; falling back to AI.",
            toolError
          );
        }
      }

      const data: any = await askTaxSarthi(userMessage);

      // For business-profile questions, use the logged-in
      // business profile directly instead of a generic AI reply.
      if (currentUser && isBusinessQuestion(userMessage)) {
        try {
          const profiles = await getBusinessProfiles();

          if (Array.isArray(profiles) && profiles.length > 0) {
            const businessAnswer = buildBusinessResponse(profiles[0]);

            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: businessAnswer,
              },
            ]);

            try {
              const result = await getChatHistory(100);
              setHistory(
                Array.isArray(result?.history)
                  ? result.history
                  : []
              );
            } catch (historyError) {
              console.warn(
                "Could not refresh chat history:",
                historyError
              );
            }

            return;
          }
        } catch (businessError) {
          console.warn(
            "Business profile lookup failed:",
            businessError
          );
        }
      }

      let aiResponse: any =
        data?.response?.answer ??
        data?.response?.text ??
        data?.response ??
        data?.answer ??
        data?.text ??
        data?.message ??
        "No response received.";

      if (
        typeof aiResponse === "object" &&
        aiResponse !== null
      ) {
        aiResponse =
          aiResponse.answer ??
          aiResponse.text ??
          aiResponse.message ??
          JSON.stringify(aiResponse);
      }
      if (!aiResponse || String(aiResponse).trim() === "") aiResponse = "TaxSarthi AI did not return a response.";
      if (typeof aiResponse === "string" && aiResponse.toLowerCase().includes("gemini error")) aiResponse = "TaxSarthi AI is temporarily unable to generate a response. Please try again.";
      setMessages((prev) => [...prev, { role: "assistant", content: cleanResponse(aiResponse) }]);
      if (currentUser) {
        try {
          const result = await getChatHistory(100);
          setHistory(
            Array.isArray(result?.history)
              ? result.history
              : []
          );
        } catch (historyError) {
          console.warn(
            "Could not refresh chat history:",
            historyError
          );
        }
      }
    } catch (error) {
      console.error("TaxSarthi AI Error:", error);
      setMessages((prev) => [...prev, { role: "assistant", content: error instanceof Error && error.message ? error.message : "Unable to connect to TaxSarthi AI. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };


  // =====================================================
  // OPEN FILE PICKER
  // =====================================================

  const openFilePicker = () => {

    if (loading) {
      return;
    }

    fileInputRef.current?.click();

  };


  // =====================================================
  // UPLOAD INVOICE
  // =====================================================

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {

    const file =
      event.target.files?.[0];


    // Reset input so same file
    // can be selected again

    event.target.value = "";


    if (!file) {
      return;
    }


    // =================================================
    // FILE TYPE VALIDATION
    // =================================================

    const allowedTypes = [
      "application/pdf",
    ];


    if (
      !allowedTypes.includes(
        file.type
      )
    ) {

      setUploadedFile({
        name: file.name,
        status: "error",
        error:
          "Please upload a PDF invoice.",
      });

      return;
    }


    // =================================================
    // FILE SIZE
    // =================================================

    const maxSize =
      10 * 1024 * 1024;


    if (
      file.size > maxSize
    ) {

      setUploadedFile({
        name: file.name,
        status: "error",
        error:
          "File size must be less than 10 MB.",
      });

      return;
    }


    // =================================================
    // SHOW UPLOADING
    // =================================================

    setUploadedFile({
      name: file.name,
      status: "uploading",
    });


    // Show uploaded file
    // in conversation

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content:
          `Uploaded invoice: ${file.name}`,
      },
    ]);


    try {

      const formData =
        new FormData();


      formData.append(
        "document_type",
        "invoice"
      );


      // Temporary backend user
      // until JWT authentication

      formData.append(
        "business_id",
        "1"
      );


      formData.append(
        "file",
        file
      );


      // =================================================
      // UPLOAD
      // =================================================

      const response =
        await fetch(
          "http://127.0.0.1:8000/documents/upload",
          {
            method: "POST",
            body: formData,
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        console.error(
          "Invoice Upload Error:",
          data
        );

        throw new Error(
          data?.detail ??
          "Invoice upload failed."
        );
      }


      // =================================================
      // ANALYSIS
      // =================================================

      const analysis =
        data?.analysis;


      setUploadedFile({
        name: file.name,
        status: "success",
        analysis,
      });


      // =================================================
      // ADD ANALYSIS RESULT TO CHAT
      // =================================================

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Your invoice has been processed and analyzed.",
          analysis,
        },
      ]);

    } catch (error) {

      console.error(
        "Invoice Upload Error:",
        error
      );


      setUploadedFile({
        name: file.name,
        status: "error",
        error:
          error instanceof Error
            ? error.message
            : "Invoice upload failed.",
      });


      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't process this invoice. Please check the file and try again.",
        },
      ]);

    }

  };


  // =====================================================
  // NEW CHAT
  // =====================================================

  const newChat = () => {

    setMessages([]);

    setMessage("");

    setUploadedFile(null);

    setLoading(false);

  };

  // =====================================================
  // DELETE ALL SAVED CHATS
  // =====================================================

  const deleteAllChats = async () => {

    if (!currentUser || history.length === 0) {
      return;
    }

    const confirmed = window.confirm(
      "Delete all saved chats? This cannot be undone."
    );

    if (!confirmed) {
      return;
    }

    try {

      setHistoryLoading(true);

      await clearChatHistory();

      setHistory([]);

      setMessages([]);

      setMessage("");

      setUploadedFile(null);

    } catch (error) {

      console.error(
        "Delete chat history error:",
        error
      );

      setLoginError(
        error instanceof Error
          ? error.message
          : "Unable to delete chat history."
      );

    } finally {

      setHistoryLoading(false);

    }

  };


  // =====================================================
  // CLOSE UPLOAD STATUS
  // =====================================================

  const clearUpload = () => {

    setUploadedFile(null);

  };


  // =====================================================
  // UI
  // =====================================================

  return (

    <main
      className={
        dark
          ? "app dark"
          : "app light"
      }
    >\n      {/* =================================================
          HIDDEN FILE INPUT
      ================================================= */}

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        onChange={
          handleFileUpload
        }
        style={{
          display: "none",
        }}
      />


      {/* =================================================
          SIDEBAR
      ================================================= */}

      <aside className="sidebar">

        <div className="sidebar-top">

          <button
            className="icon-button"
            type="button"
            aria-label="Menu"
          >
            <Menu size={20} />
          </button>


          <div className="brand-small">

            <div className="brand-mark">
              T
            </div>

            <span>
              TaxSarthi AI
            </span>

          </div>

        </div>


        <button
          className="new-chat"
          onClick={newChat}
          type="button"
        >

          <Plus size={18} />

          <span>
            New chat
          </span>

        </button>

        <nav className="sidebar-navigation" aria-label="TaxSarthi navigation">
          <Link className="history-item" href="/dashboard">
            <span>Dashboard</span>
          </Link>
          <Link className="history-item" href="/business-profile">
            <span>Business Profile</span>
          </Link>
          <Link className="history-item" href="/tools">
            <span>GST Tools</span>
          </Link>
        </nav>

        <div className="sidebar-history">
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "8px",
            }}
          >
            <p className="history-title">
              {currentUser ? "Saved chats" : "Chat"}
            </p>

            {currentUser && history.length > 0 && (
              <button
                type="button"
                onClick={deleteAllChats}
                title="Delete all saved chats"
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#999",
                  cursor: "pointer",
                  fontSize: "12px",
                }}
              >
                Delete
              </button>
            )}
          </div>
          {!currentUser && (
            <button className="history-item" type="button" onClick={() => setLoginOpen(true)}>
              <MessageSquare size={16} />
              <span>Login to save chats</span>
            </button>
          )}
          {currentUser && historyLoading && <div className="history-empty">Loading chats...</div>}
          {currentUser && !historyLoading && history.length === 0 && <div className="history-empty">No saved chats yet.</div>}
          {currentUser && !historyLoading && history.filter((item) => item.role === "user").slice(-20).reverse().map((item) => (
            <button key={item.id} className="history-item" type="button" title={item.message} onClick={() => setMessages([{ role: "user", content: item.message }])}>
              <MessageSquare size={16} />
              <span>{item.message.slice(0, 28)}{item.message.length > 28 ? "..." : ""}</span>
            </button>
          ))}
        </div>

        <div className="sidebar-bottom">

          <button
            className="theme-button"
            onClick={() =>
              setDark(!dark)
            }
            type="button"
          >

            {dark ? (
              <Sun size={18} />
            ) : (
              <Moon size={18} />
            )}

            <span>
              {dark
                ? "Light mode"
                : "Dark mode"}
            </span>

          </button>


          {currentUser ? (
            <div className="user-account">
              <div className="user-account-info">
                <div className="user-avatar">{currentUser.full_name.charAt(0).toUpperCase()}</div>
                <div className="user-account-text">
                  <strong>{currentUser.full_name}</strong>
                  <span>{currentUser.email}</span>
                </div>
              </div>
              <button className="login-button" type="button" onClick={handleLogout}>Logout</button>
            </div>
          ) : (
            <button className="login-button" type="button" onClick={() => { setLoginError(""); setLoginOpen(true); }}>Sign in</button>
          )}

        </div>

      </aside>


      {/* =================================================
          MAIN CHAT
      ================================================= */}

      <section className="chat-area">


        {/* Mobile Header */}

        <header className="mobile-header">

          <button
            className="icon-button"
            type="button"
            aria-label="Menu"
          >
            <Menu size={20} />
          </button>


          <span>
            TaxSarthi AI
          </span>


          <button
            className="icon-button"
            onClick={() =>
              setDark(!dark)
            }
            type="button"
            aria-label="Toggle theme"
          >

            {dark ? (
              <Sun size={19} />
            ) : (
              <Moon size={19} />
            )}

          </button>

        </header>


        {/* =================================================
            WELCOME
        ================================================= */}

        {messages.length === 0 ? (

          <div className="chat-content">

            <div className="welcome">

              <div className="logo-large">
                T
              </div>

              <h1>
                TaxSarthi AI
              </h1>

              <p>
                Your intelligent GST assistant
              </p>

            </div>

          </div>

        ) : (

          /* =================================================
             MESSAGES
          ================================================= */

          <div className="messages-container">

            {messages.map(
              (msg, index) => (

                <div
                  key={index}
                  className={
                    `message-row ${msg.role}`
                  }
                >

                  <div
                    className={
                      `message-avatar ${msg.role}`
                    }
                  >

                    {msg.role ===
                    "user"
                      ? "You"
                      : "T"}

                  </div>


                  <div
                    className="message-content"
                    style={{
                      whiteSpace:
                        "pre-wrap",
                    }}
                  >

                    {msg.content}

                    {msg.analysis?.success && (
                      <InvoiceAnalysisCard
                        analysis={msg.analysis}
                      />
                    )}

                  </div>

                </div>

              )
            )}


            {/* =================================================
                TYPING
            ================================================= */}

            {loading && (

              <div
                className="message-row assistant"
              >

                <div
                  className="message-avatar assistant"
                >
                  T
                </div>


                <div className="typing">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>

              </div>

            )}


            {/* =================================================
                UPLOAD STATUS
            ================================================= */}

            {uploadedFile && (

              <div
                className="upload-status"
              >

                <div
                  className="upload-status-left"
                >

                  <FileText
                    size={18}
                  />


                  <div>

                    <strong>
                      {uploadedFile.name}
                    </strong>


                    <div>

                      {uploadedFile.status ===
                        "uploading" &&
                        "Processing invoice..."}

                      {uploadedFile.status ===
                        "success" &&
                        "Invoice analyzed successfully"}

                      {uploadedFile.status ===
                        "error" &&
                        uploadedFile.error}

                    </div>

                  </div>

                </div>


                {uploadedFile.status ===
                  "success" && (

                  <CheckCircle2
                    size={20}
                  />

                )}


                {uploadedFile.status ===
                  "error" && (

                  <AlertTriangle
                    size={20}
                  />

                )}


                {uploadedFile.status !==
                  "uploading" && (

                  <button
                    type="button"
                    onClick={
                      clearUpload
                    }
                    aria-label="Clear upload"
                  >

                    <X size={16} />

                  </button>

                )}

              </div>

            )}


            <div
              ref={messagesEndRef}
            />

          </div>

        )}


        {/* =================================================
            INPUT
        ================================================= */}

        <div className="input-wrapper">

          <div className="chat-input">


            {/* Paperclip */}

            <button
              className="input-icon"
              title="Upload invoice"
              type="button"
              onClick={
                openFilePicker
              }
              disabled={loading}
            >

              <Paperclip size={20} />

            </button>


            {/* Hidden file input is above */}


            <input
              type="text"
              value={message}
              onChange={(e) =>
                setMessage(
                  e.target.value
                )
              }
              placeholder="Ask anything about GST..."
              disabled={loading}
              onKeyDown={(e) => {

                if (
                  e.key === "Enter" &&
                  !e.shiftKey
                ) {

                  e.preventDefault();

                  sendMessage();

                }

              }}
            />


            {/* Send */}

            <button
              className="send-button"
              disabled={
                !message.trim() ||
                loading
              }
              onClick={() =>
                sendMessage()
              }
              type="button"
              aria-label="Send message"
            >

              <ArrowUp size={19} />

            </button>

          </div>


          <p className="input-note">

            TaxSarthi AI can make mistakes.
            Verify important tax information.

          </p>

        </div>

      </section>

    

      {loginOpen && (
        <div className="auth-modal-backdrop" onMouseDown={(event) => {
          if (event.target === event.currentTarget) { setLoginOpen(false); setLoginError(""); }
        }}>
          <div className="auth-modal" role="dialog" aria-modal="true" aria-labelledby="login-title">
            <button className="auth-modal-close" type="button" aria-label="Close login" onClick={() => { setLoginOpen(false); setLoginError(""); }}>
              <X size={18} />
            </button>
            <div className="auth-modal-logo">T</div>
            <h2 id="login-title">Welcome back</h2>
            <p className="auth-modal-subtitle">Sign in to save chats, manage your business profile, and use personalized TaxSarthi features.</p>
            <div className="google-login-section">
              <div
                className="google-login-button"
                aria-hidden="true"
              >
                <span className="google-g-icon">G</span>
                <span>Continue with Google</span>
              </div>

              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  marginTop: "10px",
                  minHeight: "44px",
                }}
              >
                <div
                  id="google-login-button"
                  aria-label="Sign in with Google"
                />
              </div>

              <div className="auth-divider">
                <span>or</span>
              </div>
            </div>

            <form
              onSubmit={handleLogin}
              className="auth-form"
            >
              <label>
                Email
                <input
                  type="email"
                  value={loginEmail}
                  onChange={(event) =>
                    setLoginEmail(event.target.value)
                  }
                  placeholder="you@example.com"
                  autoComplete="email"
                  disabled={loginLoading}
                />
              </label>

              <label>
                Password
                <input
                  type="password"
                  value={loginPassword}
                  onChange={(event) =>
                    setLoginPassword(event.target.value)
                  }
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  disabled={loginLoading}
                />
              </label>

              {loginError && (
                <div className="auth-error">
                  {loginError}
                </div>
              )}

              <button
                type="submit"
                className="auth-submit"
                disabled={loginLoading}
              >
                {loginLoading
                  ? "Signing in..."
                  : "Sign in with email"}
              </button>
            </form>
          </div>
        </div>
      )}
</main>

  );
}