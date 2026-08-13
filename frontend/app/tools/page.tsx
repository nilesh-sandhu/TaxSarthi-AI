"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import {
  getDashboard,
  getBusinessProfiles,
  BusinessProfile,
} from "../../lib/api";

interface DashboardData {
  [key: string]: unknown;
}

export default function DashboardPage() {
  const [dashboard, setDashboard] =
    useState<DashboardData | null>(null);

  const [business, setBusiness] =
    useState<BusinessProfile | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [dashboardData, profiles] =
        await Promise.all([
          getDashboard(),
          getBusinessProfiles(),
        ]);

      setDashboard(
        dashboardData as DashboardData
      );

      if (profiles.length > 0) {
        setBusiness(profiles[0]);
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load dashboard."
      );
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-3 h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-emerald-600" />

          <p className="text-gray-600">
            Loading dashboard...
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-8">
      <div className="mx-auto max-w-7xl">

        {/* HEADER */}

        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-semibold text-emerald-600">
              TaxSarthi AI
            </p>

            <h1 className="mt-1 text-3xl font-bold text-gray-900">
              Dashboard
            </h1>

            <p className="mt-2 text-gray-600">
              Your GST and business control center.
            </p>
          </div>

          <Link
            href="/business-profile"
            className="rounded-xl bg-emerald-600 px-5 py-3 text-center font-semibold text-white transition hover:bg-emerald-700"
          >
            {business
              ? "Manage Business Profile"
              : "Add Business Profile"}
          </Link>
        </div>

        {/* ERROR */}

        {error && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        {/* BUSINESS PROFILE */}

        <section className="mb-6 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-sm text-gray-500">
                Active Business
              </p>

              <h2 className="mt-1 text-2xl font-bold text-gray-900">
                {business?.business_name ||
                  "No business profile"}
              </h2>

              {business && (
                <p className="mt-1 text-sm text-gray-500">
                  Owned by {business.owner_name}
                </p>
              )}
            </div>

            <div className="rounded-full bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700">
              {business?.business_status ||
                "Not Set"}
            </div>
          </div>

          {business ? (
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

              <InfoCard
                title="Business Type"
                value={business.business_type}
              />

              <InfoCard
                title="State"
                value={business.state}
              />

              <InfoCard
                title="Annual Turnover"
                value={`₹${Number(
                  business.turnover
                ).toLocaleString("en-IN")}`}
              />

              <InfoCard
                title="GST Status"
                value={
                  business.gstin
                    ? "Registered"
                    : "Not Registered"
                }
              />

            </div>
          ) : (
            <div className="mt-6 rounded-xl bg-gray-50 p-6 text-center">
              <p className="text-gray-600">
                Add your business profile to unlock
                personalized TaxSarthi features.
              </p>

              <Link
                href="/business-profile"
                className="mt-4 inline-block rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700"
              >
                Create Profile
              </Link>
            </div>
          )}
        </section>

        {/* QUICK ACTIONS */}

        <section className="mb-6">
          <h2 className="mb-4 text-xl font-bold text-gray-900">
            Quick Actions
          </h2>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            <ActionCard
              href="/"
              title="AI Tax Copilot"
              description="Ask GST and tax questions."
              icon="🤖"
            />

            <ActionCard
              href="/business-profile"
              title="Business Profile"
              description="Manage your business details."
              icon="🏢"
            />

            <ActionCard
              href="/"
              title="GST Calculator"
              description="Calculate GST instantly."
              icon="🧮"
            />

            <ActionCard
              href="/"
              title="HSN Search"
              description="Find HSN and GST details."
              icon="🔎"
            />

          </div>
        </section>

        {/* GST OVERVIEW */}

        <section className="mb-6">
          <h2 className="mb-4 text-xl font-bold text-gray-900">
            GST Overview
          </h2>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            <MetricCard
              title="GST Registration"
              value={
                business?.gstin
                  ? "Registered"
                  : "Review Required"
              }
            />

            <MetricCard
              title="Inter-State Supply"
              value={
                business?.interstate
                  ? "Yes"
                  : "No"
              }
            />

            <MetricCard
              title="E-commerce"
              value={
                business?.ecommerce
                  ? "Yes"
                  : "No"
              }
            />

            <MetricCard
              title="Composition Scheme"
              value={
                business?.composition_scheme
                  ? "Yes"
                  : "No"
              }
            />

          </div>
        </section>

        {/* BUSINESS INSIGHTS */}

        {business && (
          <section className="mb-6 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

            <h2 className="mb-4 text-xl font-bold text-gray-900">
              Business Snapshot
            </h2>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

              <InfoCard
                title="Registration Type"
                value={
                  business.registration_type ||
                  "Not Available"
                }
              />

              <InfoCard
                title="Business Status"
                value={
                  business.business_status
                }
              />

              <InfoCard
                title="GSTIN"
                value={
                  business.gstin ||
                  "Not Registered"
                }
              />

            </div>
          </section>
        )}

        {/* BACKEND DATA */}

        {dashboard && (
          <section className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

            <h2 className="mb-4 text-xl font-bold text-gray-900">
              TaxSarthi Data
            </h2>

            <pre className="max-h-80 overflow-auto rounded-xl bg-gray-50 p-4 text-xs text-gray-700">
              {JSON.stringify(
                dashboard,
                null,
                2
              )}
            </pre>

          </section>
        )}

      </div>
    </main>
  );
}


// =====================================================
// INFO CARD
// =====================================================

function InfoCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-gray-100 bg-gray-50 p-4">
      <p className="text-sm text-gray-500">
        {title}
      </p>

      <p className="mt-1 font-semibold text-gray-900 break-words">
        {value}
      </p>
    </div>
  );
}


// =====================================================
// METRIC CARD
// =====================================================

function MetricCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-gray-500">
        {title}
      </p>

      <p className="mt-2 text-xl font-bold text-gray-900">
        {value}
      </p>
    </div>
  );
}


// =====================================================
// ACTION CARD
// =====================================================

function ActionCard({
  href,
  title,
  description,
  icon,
}: {
  href: string;
  title: string;
  description: string;
  icon: string;
}) {
  return (
    <Link
      href={href}
      className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
    >
      <div className="text-2xl">
        {icon}
      </div>

      <h3 className="mt-3 font-bold text-gray-900">
        {title}
      </h3>

      <p className="mt-1 text-sm text-gray-600">
        {description}
      </p>
    </Link>
  );
}