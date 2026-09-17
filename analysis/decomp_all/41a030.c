
void __thiscall FUN__text__0041a030(int *param_1,undefined4 param_2,int *param_3,undefined4 param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  int *local_c;
  int *local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    if ((param_1[0x4e] == 0) &&
       (iVar2 = FUN__text__00424f80("ownDPID!=0",
                                    "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                    DAT_005ff578 + 6,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = param_3;
    *param_3 = local_8[0x4e];
    param_3[1] = -0x73607248;
    local_10 = 0;
    (**(code **)(*(int *)*local_8 + 0x68))(*local_8,local_8[0x4e],param_2,0,param_3,param_4);
    local_18 = FUN__text__0056ce80();
    local_14 = local_18;
  }
  local_8 = (int *)0x41a110;
  FUN__text__0056ce80();
  return;
}

