
undefined4 * __thiscall
FUN__text1__00844cb7(undefined4 param_1,int param_2,undefined4 param_3,int param_4)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  
  puVar1 = (undefined4 *)
           (**(code **)(param_2 + 0x20))(*(undefined4 *)(param_2 + 0x28),1,0x40,param_1);
  if (puVar1 != (undefined4 *)0x0) {
    uVar2 = (**(code **)(param_2 + 0x20))(*(undefined4 *)(param_2 + 0x28),8,0x5a0);
    puVar1[9] = uVar2;
    if (puVar1[9] == 0) {
      (**(code **)(param_2 + 0x24))(*(undefined4 *)(param_2 + 0x28),puVar1);
      puVar1 = (undefined4 *)0x0;
    }
    else {
      uVar2 = (**(code **)(param_2 + 0x20))(*(undefined4 *)(param_2 + 0x28),1,param_4);
      puVar1[10] = uVar2;
      if (puVar1[10] == 0) {
        (**(code **)(param_2 + 0x24))(*(undefined4 *)(param_2 + 0x28),puVar1[9]);
        (**(code **)(param_2 + 0x24))(*(undefined4 *)(param_2 + 0x28),puVar1);
        puVar1 = (undefined4 *)0x0;
      }
      else {
        puVar1[0xb] = puVar1[10] + param_4;
        puVar1[0xe] = param_3;
        *puVar1 = 0;
        FUN__text1__00844c00(puVar1,param_2,0);
      }
    }
  }
  return puVar1;
}

