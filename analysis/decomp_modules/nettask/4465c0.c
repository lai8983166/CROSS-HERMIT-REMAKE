
void __thiscall FUN__text__004465c0(int param_1,short param_2,short param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_78 [16];
  undefined4 local_38;
  short local_34;
  short local_30;
  short local_2c;
  short local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar3 = local_78;
  for (iVar2 = 0x1d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (int *)(param_1 + 0x8a58);
  local_8 = param_1;
  local_10 = FUN__text__00428380();
  local_14 = FUN__text__00428350();
  local_18 = FUN__text__004283b0();
  local_1c = FUN__text__00428310();
  if ((local_10 != *local_c) &&
     (iVar2 = FUN__text__00424f80("rcnt == fm->rcnt",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetTask.cpp",
                                  DAT_00606728 + 0xd,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_28 = param_2 + 7;
  local_2c = param_3 + 0x4b;
  local_24 = 0;
  for (local_20 = local_18; (local_20 != local_18 + local_14 && (local_20 < local_10));
      local_20 = local_20 + 1) {
    local_30 = local_28;
    local_34 = local_2c + (short)local_24 * 0x13;
    if (local_1c == local_20) {
      local_38 = 0xc0125a8c;
    }
    else {
      local_38 = 0x80101010;
    }
    FUN__text__00410310((int)local_28,(int)local_34,0xde,0x12,0x49,local_38,1);
    if (local_1c == local_20) {
      local_38 = 0xffc0e0ff;
    }
    else {
      local_38 = 0xffffffff;
    }
    *(undefined2 *)(local_c[1] + 0x76 + local_20 * 0x80) = 0x48;
    FUN__text__00408f10(local_30 + 2,local_34 + 2,local_38);
    local_24 = local_24 + 1;
  }
  local_8 = 0x44676b;
  FUN__text__0056ce80();
  return;
}

