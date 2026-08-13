"use client";

import { FormEvent, useEffect, useState } from "react";

import {
  BusinessProfile,
  BusinessProfileCreate,
  createBusinessProfile,
  getBusinessProfiles,
  updateBusinessProfile,
} from "../../lib/api";

export default function BusinessProfilePage() {
  const [profile, setProfile] =
    useState<BusinessProfile | null>(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] =
    useState<BusinessProfileCreate>({
      business_name: "",
      owner_name: "",
      business_type: "",
      state: "",
      turnover: 0,
      gstin: "",
      registration_type: "",
      interstate: false,
      ecommerce: false,
      composition_scheme: false,
      business_status: "Active",
    });

  // =====================================================
  // LOAD PROFILE
  // =====================================================

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      setLoading(true);
      setError("");

      const profiles = await getBusinessProfiles();

      if (profiles.length > 0) {
        const existing = profiles[0];

        setProfile(existing);

        setForm({
          business_name: existing.business_name,
          owner_name: existing.owner_name,
          business_type: existing.business_type,
          state: existing.state,
          turnover: Number(existing.turnover),
          gstin: existing.gstin || "",
          registration_type:
            existing.registration_type || "",
          interstate: existing.interstate,
          ecommerce: existing.ecommerce,
          composition_scheme:
            existing.composition_scheme,
          business_status:
            existing.business_status,
        });
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load business profile."
      );
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // UPDATE FIELD
  // =====================================================

  function updateField(
    field: keyof BusinessProfileCreate,
    value: string | number | boolean
  ) {
    setForm((previous) => ({
      ...previous,
      [field]: value,
    }));
  }

  // =====================================================
  // SUBMIT
  // =====================================================

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    try {
      setSaving(true);
      setError("");
      setSuccess("");

      let result: BusinessProfile;

      if (profile) {
        result = await updateBusinessProfile(
          profile.id,
          form
        );
      } else {
        result =
          await createBusinessProfile(form);
      }

      setProfile(result);

      setSuccess(
        profile
          ? "Business profile updated successfully."
          : "Business profile created successfully."
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to save business profile."
      );
    } finally {
      setSaving(false);
    }
  }

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">
          Loading business profile...
        </p>
      </main>
    );
  }

  // =====================================================
  // PAGE
  // =====================================================

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-10">
      <div className="mx-auto max-w-4xl">

        <div className="mb-8">
          <p className="text-sm font-semibold text-emerald-600">
            TaxSarthi AI
          </p>

          <h1 className="mt-2 text-3xl font-bold text-gray-900">
            Business Profile
          </h1>

          <p className="mt-2 text-gray-600">
            Add your business details for
            personalized GST assistance.
          </p>
        </div>

        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm md:p-8">

          <form
            onSubmit={handleSubmit}
            className="space-y-6"
          >

            {/* BUSINESS NAME */}

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Business Name
              </label>

              <input
                required
                value={form.business_name}
                onChange={(e) =>
                  updateField(
                    "business_name",
                    e.target.value
                  )
                }
                placeholder="Enter business name"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-emerald-500"
              />
            </div>

            {/* OWNER */}

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Owner Name
              </label>

              <input
                required
                value={form.owner_name}
                onChange={(e) =>
                  updateField(
                    "owner_name",
                    e.target.value
                  )
                }
                placeholder="Enter owner name"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-emerald-500"
              />
            </div>

            {/* TYPE + STATE */}

            <div className="grid gap-6 md:grid-cols-2">

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Business Type
                </label>

                <select
                  required
                  value={form.business_type}
                  onChange={(e) =>
                    updateField(
                      "business_type",
                      e.target.value
                    )
                  }
                  className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3"
                >
                  <option value="">
                    Select business type
                  </option>

                  <option value="Proprietorship">
                    Proprietorship
                  </option>

                  <option value="Partnership">
                    Partnership
                  </option>

                  <option value="LLP">
                    LLP
                  </option>

                  <option value="Private Limited">
                    Private Limited
                  </option>

                  <option value="Public Limited">
                    Public Limited
                  </option>

                  <option value="HUF">
                    HUF
                  </option>

                  <option value="Other">
                    Other
                  </option>
                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  State
                </label>

                <input
                  required
                  value={form.state}
                  onChange={(e) =>
                    updateField(
                      "state",
                      e.target.value
                    )
                  }
                  placeholder="e.g. Delhi"
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-emerald-500"
                />
              </div>

            </div>

            {/* TURNOVER */}

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Annual Turnover
              </label>

              <input
                required
                type="number"
                min="0"
                step="0.01"
                value={form.turnover}
                onChange={(e) =>
                  updateField(
                    "turnover",
                    Number(e.target.value)
                  )
                }
                placeholder="Enter annual turnover"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-emerald-500"
              />
            </div>

            {/* GSTIN */}

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                GSTIN
                <span className="ml-2 text-gray-400">
                  Optional
                </span>
              </label>

              <input
                maxLength={15}
                value={form.gstin || ""}
                onChange={(e) =>
                  updateField(
                    "gstin",
                    e.target.value.toUpperCase()
                  )
                }
                placeholder="Enter GSTIN"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 uppercase outline-none focus:border-emerald-500"
              />
            </div>

            {/* REGISTRATION */}

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Registration Type
              </label>

              <select
                value={form.registration_type || ""}
                onChange={(e) =>
                  updateField(
                    "registration_type",
                    e.target.value
                  )
                }
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3"
              >
                <option value="">
                  Select registration type
                </option>

                <option value="Regular">
                  Regular
                </option>

                <option value="Composition">
                  Composition
                </option>

                <option value="Unregistered">
                  Unregistered
                </option>
              </select>
            </div>

            {/* OPTIONS */}

            <div className="grid gap-4 md:grid-cols-3">

              <label className="flex items-center gap-3 rounded-xl border border-gray-200 p-4">
                <input
                  type="checkbox"
                  checked={form.interstate}
                  onChange={(e) =>
                    updateField(
                      "interstate",
                      e.target.checked
                    )
                  }
                />

                <span className="text-sm">
                  Interstate Business
                </span>
              </label>

              <label className="flex items-center gap-3 rounded-xl border border-gray-200 p-4">
                <input
                  type="checkbox"
                  checked={form.ecommerce}
                  onChange={(e) =>
                    updateField(
                      "ecommerce",
                      e.target.checked
                    )
                  }
                />

                <span className="text-sm">
                  E-commerce
                </span>
              </label>

              <label className="flex items-center gap-3 rounded-xl border border-gray-200 p-4">
                <input
                  type="checkbox"
                  checked={
                    form.composition_scheme
                  }
                  onChange={(e) =>
                    updateField(
                      "composition_scheme",
                      e.target.checked
                    )
                  }
                />

                <span className="text-sm">
                  Composition Scheme
                </span>
              </label>

            </div>

            {/* STATUS */}

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Business Status
              </label>

              <select
                value={form.business_status}
                onChange={(e) =>
                  updateField(
                    "business_status",
                    e.target.value
                  )
                }
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3"
              >
                <option value="Active">
                  Active
                </option>

                <option value="Inactive">
                  Inactive
                </option>
              </select>
            </div>

            {/* ERROR */}

            {error && (
              <div className="rounded-xl bg-red-50 p-4 text-sm text-red-700">
                {error}
              </div>
            )}

            {/* SUCCESS */}

            {success && (
              <div className="rounded-xl bg-green-50 p-4 text-sm text-green-700">
                {success}
              </div>
            )}

            {/* SAVE */}

            <button
              type="submit"
              disabled={saving}
              className="w-full rounded-xl bg-emerald-600 px-5 py-3.5 font-semibold text-white hover:bg-emerald-700 disabled:opacity-50"
            >
              {saving
                ? "Saving..."
                : profile
                ? "Update Business Profile"
                : "Save Business Profile"}
            </button>

          </form>
        </div>
      </div>
    </main>
  );
}