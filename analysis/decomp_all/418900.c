
void __fastcall FUN__text__00418900(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_a0 [16];
  int local_60;
  int local_5c;
  undefined4 local_58 [6];
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  int *local_8;
  
  puVar2 = local_a0;
  for (iVar1 = 0x27; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    _memset(local_58,0,0x50);
    local_58[0] = 0x50;
    local_40 = DAT_00592dd8;
    local_3c = DAT_00592ddc;
    local_38 = DAT_00592de0;
    local_34 = DAT_00592de4;
    (**(code **)(*(int *)*local_8 + 0x34))
              (*local_8,local_58,0,FUN__text__00418c20,local_8 + 0x91,0x91);
    local_60 = FUN__text__0056ce80();
    local_5c = local_60;
    if (((local_60 != -0x7788fee8) && (local_60 != -0x7788fea2)) && (local_60 != 0)) {
      FUN__text__0041b4a0(local_60);
    }
  }
  local_8 = (int *)0x4189f9;
  FUN__text__0056ce80();
  return;
}

