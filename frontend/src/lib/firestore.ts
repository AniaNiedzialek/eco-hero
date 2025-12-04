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
    // Single optimized query with limit - much faster than multiple queries
    const q = query(
      collection(db, "scan_history"),
      where("userId", "==", userId),
      orderBy("timestamp", "desc"),
      limit(100)
    );
    
    const querySnapshot = await getDocs(q);
    const docs = querySnapshot.docs;
    
    // Calculate stats from single query result
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    
    const totalScans = docs.length;
    const recyclableCount = docs.filter(doc => doc.data().recyclable).length;
    const thisMonthCount = docs.filter(doc => {
      const timestamp = doc.data().timestamp?.toDate?.();
      return timestamp && timestamp >= startOfMonth;
    }).length;

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
