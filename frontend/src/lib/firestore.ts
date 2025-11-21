import { 
  collection, 
  addDoc, 
  query, 
  where, 
  orderBy, 
  getDocs, 
  Timestamp,
  limit
} from "firebase/firestore";
import { db } from "./firebase";

export interface ScanHistoryItem {
  userId: string;
  productName: string;
  material: string;
  recyclable: boolean;
  timestamp: Date;
  barcode?: string;
  scanType: 'barcode' | 'image';
}

export interface BinReport {
  userId: string;
  latitude?: number;
  longitude?: number;
  type: string;
  description: string;
  timestamp: Date;
  status: 'pending' | 'approved' | 'rejected';
  reportType: 'new_bin' | 'issue';
  binId?: string | number;
}

// User History Functions
export const saveScanHistory = async (userId: string, data: Omit<ScanHistoryItem, 'userId' | 'timestamp'>) => {
  try {
    await addDoc(collection(db, "scan_history"), {
      ...data,
      userId,
      timestamp: Timestamp.now()
    });
  } catch (error) {
    console.error("Error saving scan history:", error);
    throw error;
  }
};

export const getUserScanHistory = async (userId: string, limitCount = 20) => {
  try {
    const q = query(
      collection(db, "scan_history"),
      where("userId", "==", userId),
      orderBy("timestamp", "desc"),
      limit(limitCount)
    );
    
    const querySnapshot = await getDocs(q);
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
      timestamp: doc.data().timestamp.toDate()
    }));
  } catch (error) {
    console.error("Error getting scan history:", error);
    throw error;
  }
};

export const getUserStats = async (userId: string) => {
  try {
    // Note: For large datasets, aggregation queries are better. 
    // For this scale, client-side counting of recent items is okay or a separate stats document.
    // We'll fetch all history for now (assuming reasonable size) or just the last 100 for a "recent" stat.
    const q = query(
      collection(db, "scan_history"),
      where("userId", "==", userId),
      orderBy("timestamp", "desc")
    );
    
    const querySnapshot = await getDocs(q);
    const docs = querySnapshot.docs;
    
    const totalScans = docs.length;
    const recyclableCount = docs.filter(doc => doc.data().recyclable).length;
    
    // Calculate this month's scans
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    const thisMonthCount = docs.filter(doc => doc.data().timestamp.toDate() >= startOfMonth).length;

    return {
      totalScans,
      recyclableCount,
      thisMonthCount
    };
  } catch (error) {
    console.error("Error getting user stats:", error);
    throw error;
  }
};

// Community Reporting Functions
export const reportBin = async (userId: string, data: Omit<BinReport, 'userId' | 'timestamp' | 'status'>) => {
  try {
    await addDoc(collection(db, "bin_reports"), {
      ...data,
      userId,
      status: 'pending',
      timestamp: Timestamp.now()
    });
  } catch (error) {
    console.error("Error reporting bin:", error);
    throw error;
  }
};
