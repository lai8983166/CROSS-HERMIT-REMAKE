
void FUN__text__0054358d(int param_1)

{
  undefined4 *puVar1;
  int iVar2;
  
  puVar1 = (undefined4 *)(*(code *)**(undefined4 **)(param_1 + 4))(param_1,0,0x5c);
  *(undefined4 **)(param_1 + 400) = puVar1;
  *puVar1 = FUN__text__00543563;
  *(undefined1 **)(*(int *)(param_1 + 400) + 4) = &LAB__text__00543209;
  *(code **)(*(int *)(param_1 + 400) + 8) = FUN__text__005433f6;
  *(code **)(*(int *)(param_1 + 400) + 0xc) = FUN__text__00542fff;
  iVar2 = 0x10;
  do {
    *(code **)(iVar2 + *(int *)(param_1 + 400)) = FUN__text__00542fff;
    iVar2 = iVar2 + 4;
  } while (iVar2 < 0x50);
  *(code **)(*(int *)(param_1 + 400) + 0x10) = FUN__text__0054255e;
  *(code **)(*(int *)(param_1 + 400) + 0x48) = FUN__text__0054279a;
  FUN__text__00543563(param_1);
  return;
}

