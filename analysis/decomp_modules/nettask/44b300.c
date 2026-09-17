
void __thiscall FUN__text__0044b300(int param_1,short param_2,short param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  uint local_1c;
  int local_18;
  uint local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((-1 < param_4) && (param_4 < 0x1e)) {
    local_c = param_1 + 0x1ab0 + param_4 * 8;
    local_10 = *(int *)(local_c + 4);
    if (*(char *)(local_c + 1) == '\0') {
      *(undefined1 *)(param_1 + 0x9f) = 0x40;
      *(undefined1 *)(param_1 + 0x9e) = 0x40;
      *(undefined1 *)(param_1 + 0x9d) = 0x40;
      *(undefined1 *)(param_1 + 0x9c) = 0x40;
    }
    else {
      *(undefined1 *)(param_1 + 0x9f) = 0x80;
      *(undefined1 *)(param_1 + 0x9e) = 0x80;
      *(undefined1 *)(param_1 + 0x9d) = 0x80;
      *(undefined1 *)(param_1 + 0x9c) = 0x80;
    }
    local_14 = (uint)*(ushort *)(local_10 + 2);
    local_8 = param_1;
    if ((0x3ff < local_14) &&
       (iVar2 = FUN__text__00424f80("(0<=char_no) && (char_no<1024)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                    DAT_00606768 + 0x23,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__0044cba0(local_8 + 0x38,0x5b,param_2 + 0x15,param_3 + 2,0x4c,local_14,&DAT_00606578);
    *(undefined1 *)(local_8 + 0x9c) = 0x80;
    *(undefined1 *)(local_8 + 0x9d) = 0x80;
    *(undefined1 *)(local_8 + 0x9e) = 0x80;
    *(undefined1 *)(local_8 + 0x9f) = 0x80;
    if ((*(short *)(local_10 + 0xc) != 0) && (*(ushort *)(local_10 + 0xc) < 0x80)) {
      if ((byte)(&DAT_006b2d8a)[(uint)*(ushort *)(local_10 + 0xc) * 0x40] == 0) {
        local_18 = 0;
      }
      else {
        local_18 = (byte)(&DAT_006b2d8a)[(uint)*(ushort *)(local_10 + 0xc) * 0x40] - 1;
      }
      FUN__text__0044cb40(local_8 + 0x38,param_2 + 1,param_3 + 1,0x4d,5,&DAT_00606580 + local_18 * 8
                         );
    }
    local_1c = (uint)*(byte *)(local_10 + 0xe);
    if (99 < local_1c) {
      local_1c = 99;
    }
    FUN__text__0044cc80(param_2 + 2,param_3 + 0x16,0x4d,local_1c,2);
    local_1c = *(int *)(local_10 + 0x20) / 0xe10;
    if (99 < (int)local_1c) {
      local_1c = 99;
    }
    FUN__text__0044cc80(param_2 + 2,param_3 + 0x26,0x4d,local_1c,2);
  }
  local_8 = 0x44b53c;
  FUN__text__0056ce80();
  return;
}

