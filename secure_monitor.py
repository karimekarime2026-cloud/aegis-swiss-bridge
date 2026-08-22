import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Union

class SecureNetworkMonitor:
    """
    نظام متقدم لمراقبة الشبكات واكتشاف الشذوذ واختراقات البيانات 
    باستخدام خوارزمية Isolation Forest. مُعد وفق المعايير الأكاديمية المتقدمة.
    """
    def __init__(self, contamination: float = 0.01, random_state: int = 42) -> None:
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(contamination=self.contamination, random_state=self.random_state)
        self.is_trained: bool = False

    def train_baseline(self, normal_network_traffic: np.ndarray) -> None:
        """تدريب النموذج على حركة المرور الطبيعية كخط أساس."""
        if normal_network_traffic.size == 0:
            raise ValueError("[ERROR]: بيانات التدريب فارغة. يرجى توفير مصفوفة بيانات صالحة.")
        self.model.fit(normal_network_traffic)
        self.is_trained = True

    def detect_anomalies(self, incoming_traffic: np.ndarray) -> Dict[str, Union[np.ndarray, int]]:
        """
        تحليل تدفق البيانات الواردة واكتشاف الشذوذ مع حساب درجات الخطورة.
        """
        if not self.is_trained:
            raise RuntimeError("[ERROR]: يجب تدريب النموذج أولاً باستخدام train_baseline.")
        if incoming_traffic.size == 0:
            raise ValueError("[ERROR]: حركة المرور الواردة فارغة.")

        predictions = self.model.predict(incoming_traffic)
        anomaly_scores = self.model.decision_function(incoming_traffic)
        anomaly_indices = np.where(predictions == -1)[0]
        
        return {
            "anomaly_indices": anomaly_indices,
            "anomaly_scores": anomaly_scores[anomaly_indices],
            "total_threats_detected": int(len(anomaly_indices))
        }
