
void __thiscall
FUN__text__00449e00(int param_1,int param_2,undefined4 param_3,int *param_4,short param_5,
                   short param_6)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_7c [16];
  undefined4 local_3c;
  short local_38;
  short local_34;
  short local_30;
  short local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_7c;
  for (iVar2 = 0x1e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x1a54;
  local_10 = param_1 + 0x1a88;
  local_8 = param_1;
  local_14 = FUN__text__00428380();
  local_18 = FUN__text__00428350();
  local_1c = FUN__text__004283b0();
  local_20 = FUN__text__00428310();
  if ((local_14 != *param_4) &&
     (iVar2 = FUN__text__00424f80("rcnt == fm->rcnt",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                  DAT_00606758 + 0xe,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_2c = param_5;
  local_30 = param_6;
  local_28 = 0;
  for (local_24 = local_1c; (local_24 != local_1c + local_18 && (local_24 < local_14));
      local_24 = local_24 + 1) {
    local_34 = local_2c;
    local_38 = local_30 + (short)local_28 * 0x12;
    if (local_20 == local_24) {
      if (param_2 == *(char *)(local_10 + 3)) {
        local_3c = 0xc0125a8c;
      }
      else {
        local_3c = 0x60092d46;
      }
    }
    else {
      local_3c = 0x80101010;
    }
    FUN__text__00410310((int)local_2c,(int)local_38,0xb9,0x11,0x49,local_3c,1);
    if (local_20 == local_24) {
      local_3c = 0xffc0e0ff;
    }
    else {
      local_3c = 0xffffffff;
    }
    *(undefined2 *)(param_4[1] + 0x76 + local_24 * 0x80) = 0x48;
    FUN__text__00408f10(local_34 + 2,local_38 + 2,local_3c);
    local_28 = local_28 + 1;
  }
  local_8 = 0x449fc0;
  FUN__text__0056ce80();
  return;
}

