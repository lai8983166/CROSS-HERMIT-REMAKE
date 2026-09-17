
void __fastcall FUN__text__00419c60(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  undefined4 *local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1[0x4e] != 0) {
    local_8 = param_1;
    FUN__text__00419de0();
    (**(code **)(*(int *)*local_8 + 0x48))(*local_8,local_8[0x4e],0,&local_10);
    local_18 = FUN__text__0056ce80();
    local_c = local_18;
    if ((local_18 == -0x7788ffe2) || (local_18 == 0)) {
      local_14 = FUN__text__00428a40(local_10);
      local_8[0x5de] = local_14;
      if ((local_8[0x5de] == 0) &&
         (iVar2 = FUN__text__00424f80("PlayerAddrBuff != 0",
                                      "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                      DAT_005ff570 + 0x13,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      (**(code **)(*(int *)*local_8 + 0x48))(*local_8,local_8[0x4e],local_8[0x5de],&local_10);
      local_c = FUN__text__0056ce80();
      if (local_c < 0) {
        FUN__text__00419de0();
      }
      else {
        (**(code **)(*(int *)local_8[1] + 0x14))
                  (local_8[1],FUN__text__00419b30,local_8[0x5de],local_10,local_8);
        local_c = FUN__text__0056ce80();
        if (local_c < 0) {
          FUN__text__00419f00();
        }
      }
    }
  }
  local_8 = (undefined4 *)0x419dd0;
  FUN__text__0056ce80();
  return;
}

