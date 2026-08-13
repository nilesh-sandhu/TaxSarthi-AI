"use client";

import React from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";

const GOOGLE_CLIENT_ID =
  process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "";

export default function GoogleAuthProviderWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <GoogleOAuthProvider
      clientId={GOOGLE_CLIENT_ID}
      onScriptLoadError={() => {
        console.error("Google Identity Services failed to load.");
      }}
      onScriptLoadSuccess={() => {
        console.log("Google Identity Services loaded.");
      }}
    >
      {children}
    </GoogleOAuthProvider>
  );
}