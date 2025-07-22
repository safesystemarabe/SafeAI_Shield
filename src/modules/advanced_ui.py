def setup_settings_tab(self):
    """لوحة الإعدادات"""
    layout = QtWidgets.QVBoxLayout(self.settings_tab)
    
    # إعدادات النظام
    system_group = QtWidgets.QGroupBox("إعدادات النظام")
    system_layout = QtWidgets.QFormLayout()
    
    self.scan_interval_spin = QtWidgets.QSpinBox()
    self.scan_interval_spin.setRange(1, 60)
    self.scan_interval_spin.setValue(self.config['system']['scan_interval'])
    
    self.threat_threshold_spin = QtWidgets.QDoubleSpinBox()
    self.threat_threshold_spin.setRange(0.1, 1.0)
    self.threat_threshold_spin.setSingleStep(0.05)
    self.threat_threshold_spin.setValue(self.config['system']['threat_threshold'])
    
    system_layout.addRow("فترة الفحص (ثواني):", self.scan_interval_spin)
    system_layout.addRow("حد التهديد:", self.threat_threshold_spin)
    system_group.setLayout(system_layout)
    layout.addWidget(system_group)
    
    # إعدادات البلوكتشين
    blockchain_group = QtWidgets.QGroupBox("إعدادات البلوكتشين")
    blockchain_layout = QtWidgets.QFormLayout()
    
    self.blockchain_enable = QtWidgets.QCheckBox("تفعيل البلوكتشين")
    self.blockchain_enable.setChecked(self.config['blockchain']['enable'])
    
    self.infura_id_edit = QtWidgets.QLineEdit(self.config['blockchain']['infura_project_id'])
    self.contract_address_edit = QtWidgets.QLineEdit(self.config['blockchain']['contract_address'])
    self.private_key_edit = QtWidgets.QLineEdit()
    self.private_key_edit.setEchoMode(QtWidgets.QLineEdit.Password)
    self.private_key_edit.setPlaceholderText("أدخل المفتاح الخاص (لا يتم تخزينه)")
    
    blockchain_layout.addRow("التفعيل:", self.blockchain_enable)
    blockchain_layout.addRow("معرف Infura:", self.infura_id_edit)
    blockchain_layout.addRow("عنوان العقد:", self.contract_address_edit)
    blockchain_layout.addRow("المفتاح الخاص:", self.private_key_edit)
    blockchain_group.setLayout(blockchain_layout)
    layout.addWidget(blockchain_group)
    
    # إعدادات السحابة
    cloud_group = QtWidgets.QGroupBox("إعدادات النسخ الاحتياطي السحابي")
    cloud_layout = QtWidgets.QFormLayout()
    
    self.cloud_enable = QtWidgets.QCheckBox("تفعيل النسخ الاحتياطي السحابي")
    self.cloud_enable.setChecked(self.config['cloud']['enable'])
    
    self.dropbox_token_edit = QtWidgets.QLineEdit()
    self.dropbox_token_edit.setEchoMode(QtWidgets.QLineEdit.Password)
    self.dropbox_token_edit.setPlaceholderText("أدخل رمز Dropbox (لا يتم تخزينه)")
    
    cloud_layout.addRow("التفعيل:", self.cloud_enable)
    cloud_layout.addRow("رمز Dropbox:", self.dropbox_token_edit)
    cloud_group.setLayout(cloud_layout)
    layout.addWidget(cloud_group)
    
    # إعدادات SIEM
    siem_group = QtWidgets.QGroupBox("إعدادات SIEM")
    siem_layout = QtWidgets.QFormLayout()
    
    self.siem_enable = QtWidgets.QCheckBox("تفعيل SIEM")
    self.siem_enable.setChecked(self.config['siem']['enable'])
    
    self.elastic_url_edit = QtWidgets.QLineEdit(self.config['siem']['elasticsearch_url'])
    self.index_name_edit = QtWidgets.QLineEdit(self.config['siem']['index_name'])
    
    siem_layout.addRow("التفعيل:", self.siem_enable)
    siem_layout.addRow("رابط Elasticsearch:", self.elastic_url_edit)
    siem_layout.addRow("اسم الفهرس:", self.index_name_edit)
    siem_group.setLayout(siem_layout)
    layout.addWidget(siem_group)
    
    # إعدادات الأمان
    security_group = QtWidgets.QGroupBox("إعدادات الأمان")
    security_layout = QtWidgets.QFormLayout()
    
    self.whitelist_edit = QtWidgets.QPlainTextEdit()
    self.whitelist_edit.setPlainText("\n".join(self.config['security']['whitelisted_processes']))
    
    security_layout.addRow("العمليات المسموحة:", self.whitelist_edit)
    security_group.setLayout(security_layout)
    layout.addWidget(security_group)
    
    # زر الحفظ
    save_btn = QtWidgets.QPushButton("حفظ الإعدادات")
    save_btn.clicked.connect(self.save_settings)
    layout.addWidget(save_btn)
    
def save_settings(self):
    """حفظ الإعدادات المحدثة"""
    try:
        # تحديث إعدادات النظام
        self.config['system']['scan_interval'] = self.scan_interval_spin.value()
        self.config['system']['threat_threshold'] = self.threat_threshold_spin.value()
        
        # تحديث إعدادات البلوكتشين
        self.config['blockchain']['enable'] = self.blockchain_enable.isChecked()
        self.config['blockchain']['infura_project_id'] = self.infura_id_edit.text()
        self.config['blockchain']['contract_address'] = self.contract_address_edit.text()
        
        # إذا تم إدخال مفتاح خاص جديد
        if self.private_key_edit.text():
            self.config['blockchain']['private_key'] = self.private_key_edit.text()
            
        # تحديث إعدادات السحابة
        self.config['cloud']['enable'] = self.cloud_enable.isChecked()
        if self.dropbox_token_edit.text():
            self.config['cloud']['dropbox_token'] = self.dropbox_token_edit.text()
            
        # تحديث إعدادات SIEM
        self.config['siem']['enable'] = self.siem_enable.isChecked()
        self.config['siem']['elasticsearch_url'] = self.elastic_url_edit.text()
        self.config['siem']['index_name'] = self.index_name_edit.text()
        
        # تحديث إعدادات الأمان
        whitelist_text = self.whitelist_edit.toPlainText()
        self.config['security']['whitelisted_processes'] = [
            line.strip() for line in whitelist_text.split('\n') if line.strip()
        ]
        
        # الحفظ عبر ConfigManager
        from modules.config_manager import ConfigManager
        config_manager = ConfigManager()
        config_manager.save_config(self.config)
        
        QtWidgets.QMessageBox.information(self, "تم الحفظ", "تم حفظ الإعدادات بنجاح!")
    except Exception as e:
        QtWidgets.QMessageBox.critical(self, "خطأ", f"فشل في حفظ الإعدادات: {str(e)}")