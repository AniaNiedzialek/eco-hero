// src/lib/api.ts

export type Resource = { program: string; ref: string };

const BASE = import.meta.env.VITE_API_BASE ?? "";
console.log("[api] BASE =", BASE); // temporary debug

async function ok<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let msg = "Request failed";
    try {
      const body: any = await res.json();
      msg = body?.detail?.message ?? body?.message ?? msg;
    } catch {}
    throw new Error(msg);
  }
  return (res.json() as unknown) as T;
}

export const api = {
  rules: (zip: string) =>
    fetch(`${BASE}/api/rules/${encodeURIComponent(zip)}`).then(ok<any>),

  schedule: (q: { address: string; zip_code: string }) =>
    fetch(
      `${BASE}/api/collection/schedule?address=${encodeURIComponent(
        q.address
      )}&zip_code=${encodeURIComponent(q.zip_code)}`
    ).then(ok<any>),

  notify: (payload: { email: string; address: string; zip_code: string }) =>
    fetch(
      `${BASE}/api/collection/notify?email=${encodeURIComponent(
        payload.email
      )}&address=${encodeURIComponent(
        payload.address
      )}&zip_code=${encodeURIComponent(payload.zip_code)}`,
      { method: "POST" }
    ).then(ok<any>),

  scanUpload: (file: File, zip: string): Promise<Resource[]> => {
    const fd = new FormData();
    fd.append("file", file);
    return fetch(
      `${BASE}/api/scanner/uploadfile/?zip_code=${encodeURIComponent(zip)}`,
      { method: "POST", body: fd }
    ).then(ok<Resource[]>);
  },

  scanBarcode: (barcode: string, zip: string): Promise<Resource[]> =>
    fetch(
      `${BASE}/api/scanner/scanbarcode/?zip_code=${encodeURIComponent(
        zip
      )}&barcode=${encodeURIComponent(barcode)}`
    ).then(ok<Resource[]>),

  binsNear: (addr: string, radius = 5, max = 10) =>
    fetch(
      `${BASE}/api/bin/near?addr=${encodeURIComponent(
        addr
      )}&radius_miles=${radius}&max_results=${max}`
    ).then(ok<any>),
};
