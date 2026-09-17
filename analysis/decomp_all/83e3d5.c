
undefined4
FUN__text1__0083e3d5
          (int param_1,int param_2,int param_3,int param_4,int param_5,int param_6,char *param_7,
          int param_8)

{
  undefined4 uVar1;
  int *piVar2;
  int iVar3;
  bool bVar4;
  uint local_10;
  
  if (((param_7 == (char *)0x0) || (*param_7 != *PTR_s_1_1_4_0086eda8)) || (param_8 != 0x38)) {
    uVar1 = 0xfffffffa;
  }
  else if (param_1 == 0) {
    uVar1 = 0xfffffffe;
  }
  else {
    *(undefined4 *)(param_1 + 0x18) = 0;
    if (*(int *)(param_1 + 0x20) == 0) {
      *(code **)(param_1 + 0x20) = FUN__text1__0084153e;
      *(undefined4 *)(param_1 + 0x28) = 0;
    }
    if (*(int *)(param_1 + 0x24) == 0) {
      *(code **)(param_1 + 0x24) = FUN__text1__00841567;
    }
    if (param_2 == -1) {
      param_2 = 6;
    }
    bVar4 = param_4 < 0;
    if (bVar4) {
      param_4 = -param_4;
    }
    local_10 = (uint)bVar4;
    if (((((param_5 < 1) || (9 < param_5)) || ((param_3 != 8 || ((param_4 < 9 || (0xf < param_4)))))
         ) || (param_2 < 0)) || (((9 < param_2 || (param_6 < 0)) || (2 < param_6)))) {
      uVar1 = 0xfffffffe;
    }
    else {
      piVar2 = (int *)(**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),1,0x16b8);
      if (piVar2 == (int *)0x0) {
        uVar1 = 0xfffffffc;
      }
      else {
        *(int **)(param_1 + 0x1c) = piVar2;
        *piVar2 = param_1;
        piVar2[6] = local_10;
        piVar2[10] = param_4;
        piVar2[9] = 1 << ((byte)piVar2[10] & 0x1f);
        piVar2[0xb] = piVar2[9] + -1;
        piVar2[0x12] = param_5 + 7;
        piVar2[0x11] = 1 << ((byte)piVar2[0x12] & 0x1f);
        piVar2[0x13] = piVar2[0x11] + -1;
        piVar2[0x14] = (piVar2[0x12] + 2U) / 3;
        iVar3 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),piVar2[9],2);
        piVar2[0xc] = iVar3;
        iVar3 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),piVar2[9],2);
        piVar2[0xe] = iVar3;
        iVar3 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),piVar2[0x11],2);
        piVar2[0xf] = iVar3;
        piVar2[0x5a5] = 1 << ((char)param_5 + 6U & 0x1f);
        iVar3 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),piVar2[0x5a5],4);
        piVar2[2] = iVar3;
        piVar2[3] = piVar2[0x5a5] << 2;
        if (((piVar2[0xc] == 0) || (piVar2[0xe] == 0)) || ((piVar2[0xf] == 0 || (piVar2[2] == 0))))
        {
          *(undefined **)(param_1 + 0x18) = PTR_s_insufficient_memory_0086ee44;
          FUN__text1__0083eee5(param_1);
          uVar1 = 0xfffffffc;
        }
        else {
          piVar2[0x5a7] = iVar3 + (piVar2[0x5a5] & 0xfffffffeU);
          piVar2[0x5a4] = piVar2[2] + piVar2[0x5a5] * 3;
          piVar2[0x1f] = param_2;
          piVar2[0x20] = param_6;
          *(undefined1 *)((int)piVar2 + 0x1d) = 8;
          uVar1 = FUN__text1__0083e861(param_1);
        }
      }
    }
  }
  return uVar1;
}

