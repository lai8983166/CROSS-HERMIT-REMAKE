
undefined4 * FUN__text__0055cb26(int param_1,undefined4 param_2,int param_3)

{
  undefined4 *puVar1;
  int iVar2;
  
  puVar1 = (undefined4 *)(**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),1,0x40);
  if (puVar1 != (undefined4 *)0x0) {
    iVar2 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),8,0x5a0);
    puVar1[9] = iVar2;
    if (iVar2 != 0) {
      iVar2 = (**(code **)(param_1 + 0x20))(*(undefined4 *)(param_1 + 0x28),1,param_3);
      puVar1[10] = iVar2;
      if (iVar2 == 0) {
        (**(code **)(param_1 + 0x24))(*(undefined4 *)(param_1 + 0x28),puVar1[9]);
        (**(code **)(param_1 + 0x24))(*(undefined4 *)(param_1 + 0x28),puVar1);
        return (undefined4 *)0x0;
      }
      *puVar1 = 0;
      puVar1[0xb] = iVar2 + param_3;
      puVar1[0xe] = param_2;
      FUN__text__0055cabb(puVar1,param_1,0);
      return puVar1;
    }
    (**(code **)(param_1 + 0x24))(*(undefined4 *)(param_1 + 0x28),puVar1);
  }
  return (undefined4 *)0x0;
}

