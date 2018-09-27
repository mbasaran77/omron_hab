from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils



class modBusWriteRead():
    def __init__(self,client_host):
        self.client_host = client_host
        self.client_port = 502
        self.err_list = []
        self.connect() #buradan bağlantı yapılacak;

    def connect(self):
        self.modbus_c = ModbusClient()
        self.modbus_c.host(self.client_host)
        self.modbus_c.port(self.client_port)
        if not self.modbus_c.is_open():
            if not self.modbus_c.open():
                text="unable to connect to " + self.client_host + ":" + str(self.client_port)
                print(text)

    def write_data_reg(self,address,list):
        if self.modbus_c.open():
            if len(list)>120:
                sent_list = self.hazirla_dizi_to_write(list)
                i = 0
                hedef_reg_taban = address
                for list_to_sent in sent_list:
                    hedef_reg = hedef_reg_taban + (i * 120)
                    a = self.modbus_c.write_multiple_registers(hedef_reg, list_to_sent)
                    if a == None or a == False:
                        self.err_list.append(False)
                    i += 1
            else:
                a = self.modbus_c.write_multiple_registers(address, list)
                if a == None or a == False:
                    self.err_list.append(False)
        if len(self.err_list) > 0:
            self.err_list = []
            pass
            # dikkat
            # print("data göndermede hata oluştu, tekrar deneyin !")

    def hazirla_dizi_to_write(self,d_list):
        # eğer gönderilecek değer 120 den büyük ise aşağıdaki fonksiyon 120 lik diziler döndürüyor
        r_list = []
        g_list = []
        i = 0
        for index in range(len(d_list)):
            g_list.append(d_list[index])
            i += 1
            if i > 119:
                i = 0
                r_list.append(g_list)
                g_list = []
            if (len(d_list) - 1) == index and i < 119:
                r_list.append(g_list)
        return r_list

    def read_data_reg(self,address,reg_count,read_float=False ):
        # burada 16 lık ya da float olarak okunabiliyor
        if self.modbus_c.is_open():
            if read_float == False:
                plc_list_int = self.modbus_c.read_holding_registers(address, reg_count)
                return plc_list_int
            elif read_float == True:
                plc_list_f_16=self.modbus_c.read_holding_registers(address,reg_count)
                if plc_list_f_16 is not None:
                    plc_list_float=self.long_to_float(plc_list_f_16)
                    return plc_list_float

    def long_to_float(self,list_16):
        list_float=[]
        list_16.reverse()
        list_long=utils.word_list_to_long(list_16)
        for any_long in list_long:
            list_float.append(utils.decode_ieee(any_long))
        list_float.reverse()
        return list_float



plc = modBusWriteRead("192.168.250.3")

deneme = plc.read_data_reg(0, 10, False)

print(deneme)